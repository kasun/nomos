"""Tool abstractions and related logic for the Nomos package."""

import asyncio
import inspect
from concurrent.futures import Future
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    Union,
    cast,
)

from docstring_parser import parse
from pydantic import BaseModel, ValidationError

from ..utils.utils import create_base_model, parse_type


class ArgDef(BaseModel):
    """Documentation for an argument of a tool."""

    key: str  # Name of the argument
    desc: Optional[str] = None  # Description of the argument
    type: Optional[str] = (
        None  # Type of the argument (e.g., "str", "int", "float", "bool", "List[str]", etc.)
    )

    def get_type(self) -> Optional[Type]:
        return parse_type(self.type) if self.type else None


class ToolDef(BaseModel):
    """Documentation for a tool."""

    desc: Optional[str] = None  # Description of the tool
    args: List[ArgDef]  # Argument descriptions for the tool


class Tool(BaseModel):
    """
    Represents a tool that can be used in the agent's flow.

    Attributes:
        name (str): The name of the tool.
        description (str): A brief description of the tool.
        function (Callable): The function to be executed when the tool is called.
        parameters (Dict[str, Dict[str, Any]]): A dictionary of parameters for the function.
    Methods:
        from_function(function: Callable, tool_arg_descs: Dict[str, Dict[str, str]]) -> Tool:
            Create a Tool instance from a function and its argument descriptions.
        from_pkg(identifier: str, tool_arg_descs: Dict[str, Dict[str, str]]) -> Tool:
            Create a Tool instance from a package identifier.
        get_args_model() -> Type[BaseModel]:
            Get the Pydantic model for the tool's arguments.
        run(**kwargs) -> str:
            Execute the tool with the provided arguments.
    """

    name: str
    description: str
    function: Callable
    parameters: Dict[str, Dict[str, Any]] = {}
    args_model: Optional[Type[BaseModel]] = None

    def __hash__(self) -> int:
        """Get the hash of the Tool instance based on its name."""
        return hash(self.name)

    @classmethod
    def from_function(
        cls,
        function: Callable,
        tool_defs: Optional[Dict[str, ToolDef]] = None,
        name: Optional[str] = None,
    ) -> "Tool":
        """
        Create a Tool instance from a function and its argument descriptions.

        :param function: The function to be executed when the tool is called.
        :param tool_arg_descs: A dictionary of argument descriptions for the function.
        :return: An instance of Tool.
        """
        sig = inspect.signature(function)
        name = name or function.__name__
        description = (
            parse(function.__doc__.strip()).short_description if function.__doc__ else None
        ) or ""

        _doc_params = parse(function.__doc__.strip()).params if function.__doc__ else []
        tool_arg_defs = {
            param.arg_name: {
                "description": param.description,
                "type": param.type_name,
            }
            for param in _doc_params
        }
        if tool_defs is not None and name in tool_defs:
            tool_def = tool_defs[name]
            description = tool_def.desc or description
            for arg in tool_def.args or []:
                tool_arg_defs[arg.key] = {
                    "description": arg.desc or tool_arg_defs.get(arg.key, {}).get("description"),
                    "type": arg.type or tool_arg_defs.get(arg.key, {}).get("type"),
                }

        params = {}
        for _name, param in sig.parameters.items():
            _type = (
                param.annotation
                if param.annotation is not inspect.Parameter.empty
                else tool_arg_defs.get(_name, {}).get("type")
            )
            _description = tool_arg_defs.get(_name, {}).get("description")
            assert _type is not None, (
                f"Type for parameter '{_name}' cannot be None. Please provide a valid type using "
                "`tool.tool_defs`, add a type annotation to the function or write a docstring for the function."
            )
            _type = parse_type(_type) if isinstance(_type, str) else _type
            params[_name] = {
                "type": _type,
            }
            if _description:
                params[_name]["description"] = _description
            if param.default is not inspect.Parameter.empty:
                params[_name]["default"] = param.default

        return cls(
            name=name,
            description=description,
            function=function,
            parameters=params,
        )

    @classmethod
    def from_pkg(
        cls,
        name: str,
        identifier: str,
        tool_defs: Optional[Dict[str, ToolDef]] = None,
    ) -> "Tool":
        """
        Create a Tool instance from a package identifier.

        :param identifier: The package identifier in the format "itertools.combinations", "package.submodule.submodule.function", etc.
        """
        if "." not in identifier:
            raise ValueError(
                f"Invalid tool identifier: {identifier}. It should be in the format 'package.submodule.function'."
            )
        module_name, function_name = identifier.rsplit(".", 1)
        try:
            module = __import__(module_name, fromlist=[function_name])
            function = getattr(module, function_name, None)
            assert function is not None, (
                f"Function '{function_name}' not found in module '{module_name}'."
            )
            assert callable(function), (
                f"'{function_name}' in module '{module_name}' is not callable."
            )
            return cls.from_function(function, tool_defs, name)
        except Exception as e:
            raise ValueError(f"Could not load tool {identifier}: {e}")

    @classmethod
    def from_langchain_tool(cls) -> None:
        """TODO: Create a Tool instance from a LangChain tool."""
        return

    @classmethod
    def from_crewai_tool(
        cls, name: str, tool_id: str, tool_kwargs: Optional[dict] = None
    ) -> "Tool":
        """
        Create a Tool instance from a CrewAI tool.

        :param tool_id: The ID of the CrewAI tool. eg- FileReadTool
        :param tool_kwargs: Optional keyword arguments for the CrewAI tool.
        :return: An instance of Tool.
        """
        from crewai.tools import BaseTool
        from pydantic import BaseModel, ConfigDict, create_model

        def rename_pydantic_model(model: type[BaseModel], new_name: str) -> type[BaseModel]:
            """Rename a Pydantic model while preserving its fields and defaults."""
            fields = {name: (field.annotation, field) for name, field in model.model_fields.items()}
            return create_model(new_name, **fields, __config__=ConfigDict(extra="forbid"))

        tool_kwargs = tool_kwargs or {}

        module = __import__("crewai_tools", fromlist=[tool_id])
        tool_class = getattr(module, tool_id, None)
        assert tool_class is not None, f"Tool class {tool_id} not found in crewai_tools module"

        try:
            tool_instance = tool_class(**tool_kwargs)
            assert isinstance(tool_instance, BaseTool), f"{tool_id} is not a valid CrewAI tool"
            structured_tool = tool_instance.to_structured_tool()
            camel_case_fn_name = name.replace("_", " ").title().replace(" ", "")
            new_tool_args_model = rename_pydantic_model(
                structured_tool.args_schema, f"{camel_case_fn_name}Args"
            )
            return cls(
                name=name,
                description=tool_instance.name,
                function=tool_instance.run,
                parameters={},
                args_model=new_tool_args_model,
            )
        except Exception as e:
            raise ValueError(f"Could not load CrewAI tool {tool_id}: {e}")

    def get_args_model(self) -> Type[BaseModel]:
        """
        Get the Pydantic model for the tool's arguments.

        :return: A Pydantic model representing the tool's arguments.
        """
        if self.args_model:
            return self.args_model
        camel_case_fn_name = self.name.replace("_", " ").title().replace(" ", "")
        basemodel_name = f"{camel_case_fn_name}Args"
        description = f"Arguments for the {self.name} tool."
        args_model = create_base_model(
            basemodel_name,
            self.parameters,
            desc=description,
        )
        self.args_model = args_model
        return args_model

    def run(self, *args, **kwargs) -> str:
        """
        Execute the tool with the provided arguments.

        :param kwargs: The arguments to be passed to the tool's function.
        :return: The result of the tool's function.
        """
        # Validate the arguments
        args_model = self.get_args_model()
        try:
            args_model(**kwargs)
        except ValidationError as e:
            raise InvalidArgumentsError(e)

        result = self.function(*args, **kwargs)
        if inspect.iscoroutine(result) or isinstance(result, asyncio.Future):
            result = asyncio.run(cast(Coroutine[Any, Any, Any], result))
        elif isinstance(result, Future):
            result = result.result()

        return str(result)

    def __str__(self) -> str:
        """String representation of the Tool instance."""
        return f"Tool(name={self.name}, description={self.description})"


class FallbackError(Exception):
    """
    Fallback Instruction if a tool fails.

    So the agent can continue the flow.
    """

    def __init__(self, error: str, fallback: str) -> None:
        """
        Agent fallback exception.

        :param error: The error message.
        :param fallback: The fallback instruction.
        """
        super().__init__(error)
        self.error = error
        self.fallback = fallback

    def __str__(self) -> str:
        """Create a simplified validation error."""
        return f"Ran into an error: {self.error}. Follow this fallback instruction: {self.fallback}"


class InvalidArgumentsError(Exception):
    """Exception raised when an invalid argument is passed to a tool."""

    def __init__(self, error: ValidationError) -> None:
        """
        Invalid argument exception.

        :param error: The error message.
        """
        super().__init__(str(error))
        self.error = error

    def __str__(self) -> str:
        """Create a simplified validation error."""
        errors = self.error.errors()
        error_messages = []
        for error in errors:
            msg = error.get("msg")
            error_messages.append(msg) if msg else None
        return f"Invalid arguments: {', '.join(error_messages)}. Please Try again with valid arguments."


class ToolWrapper(BaseModel):
    """Represents a wrapper for a tool."""

    tool_type: Literal["pkg", "crewai", "langchain"]
    tool_identifier: str
    name: str
    kwargs: Optional[dict] = None

    def get_tool(self, tool_defs: Optional[Dict[str, ToolDef]] = None) -> Tool:
        """
        Get a Tool instance from the tool identifier.

        :return: An instance of Tool.
        """
        if self.tool_type == "pkg":
            return Tool.from_pkg(
                name=self.name,
                identifier=self.tool_identifier,
                tool_defs=tool_defs,
            )
        if self.tool_type == "crewai":
            return Tool.from_crewai_tool(
                name=self.name, tool_id=self.tool_identifier, tool_kwargs=self.kwargs
            )
        # if self.tool_type == "langchain":
        #     return Tool.from_langchain_tool(
        #         name=self.name, tool=self.tool_identifier, tool_kwargs=self.kwargs
        #     )
        raise ValueError(
            f"Unsupported tool type: {self.tool_type}. Supported types are 'pkg', 'crewai', and 'langchain'."
        )


def get_tools(
    tools: Optional[list[Union[Callable, ToolWrapper]]],
    tool_defs: Optional[Dict[str, ToolDef]] = None,
) -> dict[str, Tool]:
    """
    Get a list of Tool instances from a list of functions or tool identifiers.

    :param tools: A list of functions or tool identifiers.
    :param tool_defs: Optional dictionary of tool definitions for argument descriptions.
    :return: A dictionary mapping tool names to Tool instances.
    """
    _tools: dict[str, Tool] = {}
    for tool in tools or []:
        _tool = None
        if callable(tool):
            _tool = Tool.from_function(tool, tool_defs)
        if isinstance(tool, ToolWrapper):
            _tool = tool.get_tool(tool_defs)
        assert _tool is not None, "Tool must be a callable or a ToolWrapper instance"
        _tools[_tool.name] = _tool
    return _tools


__all__ = [
    "Tool",
    "FallbackError",
    "get_tools",
    "ToolWrapper",
]
