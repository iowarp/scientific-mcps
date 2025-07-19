"""
Beautiful output formatting utilities for Jarvis MCP server.
Provides structured, readable, and visually appealing output formatting.
"""
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class JarvisFormatter:
    """
    A comprehensive formatter for creating beautiful, structured output
    that enhances readability and provides consistent formatting across
    all Jarvis MCP operations.
    """
    
    @staticmethod
    def format_success_response(
        operation: str,
        data: Any,
        summary: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        insights: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Format a successful operation response with beautiful structure.
        
        Args:
            operation: Name of the operation performed
            data: Main data result
            summary: Summary statistics or information
            metadata: Additional metadata about the operation
            insights: Key insights or recommendations
            
        Returns:
            Beautifully formatted response dictionary
        """
        response: Dict[str, Any] = {
            "🤖 Operation": operation.replace("_", " ").title(),
            "✅ Status": "Success",
            "⏰ Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "📦 Jarvis Data": JarvisFormatter._format_jarvis_data(data)
        }
        
        if summary:
            response["📊 Summary"] = JarvisFormatter._format_summary(summary)
            
        if metadata:
            response["🔍 Metadata"] = JarvisFormatter._format_metadata(metadata)
            
        if insights:
            response["💡 Insights"] = JarvisFormatter._format_insights(insights)
            
        return response
    
    @staticmethod
    def format_error_response(
        operation: str,
        error_message: str,
        error_type: str,
        suggestions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Format an error response with helpful information.
        
        Args:
            operation: Name of the operation that failed
            error_message: Detailed error message
            error_type: Type of error that occurred
            suggestions: Suggested solutions or next steps
            
        Returns:
            Beautifully formatted error response
        """
        response: Dict[str, Any] = {
            "🤖 Operation": operation.replace("_", " ").title(),
            "❌ Status": "Error",
            "⏰ Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "🚨 Error Type": error_type,
            "📝 Error Message": error_message
        }
        
        if suggestions:
            response["💭 Suggestions"] = JarvisFormatter._format_suggestions(suggestions)
            
        return response
    
    @staticmethod
    def _format_jarvis_data(data: Any) -> Any:
        """Format Jarvis data with appropriate structure."""
        if isinstance(data, dict):
            return JarvisFormatter._format_dict(data)
        elif isinstance(data, list):
            return JarvisFormatter._format_list(data)
        else:
            return data
    
    @staticmethod
    def _format_dict(data: Dict) -> Dict:
        """Format dictionary with nested structure handling."""
        formatted = {}
        for key, value in data.items():
            # Add appropriate emoji prefixes for common Jarvis items
            if "package" in key.lower():
                formatted_key = f"📦 {key.replace('_', ' ').title()}"
            elif "repository" in key.lower() or "repo" in key.lower():
                formatted_key = f"🗂️ {key.replace('_', ' ').title()}"
            elif "service" in key.lower():
                formatted_key = f"⚙️ {key.replace('_', ' ').title()}"
            elif "application" in key.lower():
                formatted_key = f"🚀 {key.replace('_', ' ').title()}"
            elif "interceptor" in key.lower():
                formatted_key = f"🔍 {key.replace('_', ' ').title()}"
            elif "resource" in key.lower():
                formatted_key = f"💻 {key.replace('_', ' ').title()}"
            elif "hardware" in key.lower():
                formatted_key = f"🖥️ {key.replace('_', ' ').title()}"
            elif "network" in key.lower():
                formatted_key = f"🌐 {key.replace('_', ' ').title()}"
            elif "storage" in key.lower():
                formatted_key = f"💾 {key.replace('_', ' ').title()}"
            elif "config" in key.lower() or "parameter" in key.lower():
                formatted_key = f"⚙️ {key.replace('_', ' ').title()}"
            elif "dependency" in key.lower():
                formatted_key = f"🔗 {key.replace('_', ' ').title()}"
            elif "capability" in key.lower():
                formatted_key = f"⭐ {key.replace('_', ' ').title()}"
            elif "description" in key.lower():
                formatted_key = f"📝 {key.replace('_', ' ').title()}"
            elif "type" in key.lower():
                formatted_key = f"🏷️ {key.replace('_', ' ').title()}"
            elif "status" in key.lower():
                formatted_key = f"📊 {key.replace('_', ' ').title()}"
            elif "health" in key.lower():
                formatted_key = f"❤️ {key.replace('_', ' ').title()}"
            elif "priority" in key.lower():
                formatted_key = f"🔝 {key.replace('_', ' ').title()}"
            elif "count" in key.lower():
                formatted_key = f"📊 {key.replace('_', ' ').title()}"
            elif "error" in key.lower():
                formatted_key = f"🚨 {key.replace('_', ' ').title()}"
            elif "warning" in key.lower():
                formatted_key = f"⚠️ {key.replace('_', ' ').title()}"
            elif "success" in key.lower():
                formatted_key = f"✅ {key.replace('_', ' ').title()}"
            elif "path" in key.lower():
                formatted_key = f"📁 {key.replace('_', ' ').title()}"
            elif "example" in key.lower():
                formatted_key = f"💡 {key.replace('_', ' ').title()}"
            elif "recommendation" in key.lower():
                formatted_key = f"🎯 {key.replace('_', ' ').title()}"
            elif "combination" in key.lower():
                formatted_key = f"🔗 {key.replace('_', ' ').title()}"
            else:
                formatted_key = f"🔧 {key.replace('_', ' ').title()}"
            
            if isinstance(value, (dict, list)):
                formatted[formatted_key] = JarvisFormatter._format_jarvis_data(value)
            else:
                formatted[formatted_key] = value
        return formatted
    
    @staticmethod
    def _format_list(data: List) -> List:
        """Format list with appropriate item formatting."""
        return [JarvisFormatter._format_jarvis_data(item) for item in data]
    
    @staticmethod
    def _format_summary(summary: Dict) -> Dict:
        """Format summary information with visual enhancements."""
        formatted_summary = {}
        
        for key, value in summary.items():
            # Add appropriate emoji prefixes for common summary items
            if "total" in key.lower():
                formatted_key = f"📈 {key.replace('_', ' ').title()}"
            elif "count" in key.lower():
                formatted_key = f"📊 {key.replace('_', ' ').title()}"
            elif "package" in key.lower():
                formatted_key = f"📦 {key.replace('_', ' ').title()}"
            elif "repository" in key.lower() or "repo" in key.lower():
                formatted_key = f"🗂️ {key.replace('_', ' ').title()}"
            elif "error" in key.lower():
                formatted_key = f"🚨 {key.replace('_', ' ').title()}"
            elif "success" in key.lower():
                formatted_key = f"✅ {key.replace('_', ' ').title()}"
            elif "status" in key.lower():
                formatted_key = f"📊 {key.replace('_', ' ').title()}"
            elif "operation" in key.lower():
                formatted_key = f"⚙️ {key.replace('_', ' ').title()}"
            elif "type" in key.lower():
                formatted_key = f"🏷️ {key.replace('_', ' ').title()}"
            else:
                formatted_key = f"📋 {key.replace('_', ' ').title()}"
            
            formatted_summary[formatted_key] = value
        
        return formatted_summary
    
    @staticmethod
    def _format_metadata(metadata: Dict) -> Dict:
        """Format metadata with visual enhancements."""
        formatted_metadata = {}
        
        for key, value in metadata.items():
            # Add appropriate emoji prefixes for metadata items
            if "jarvis" in key.lower():
                formatted_key = f"🤖 {key.replace('_', ' ').title()}"
            elif "resource" in key.lower():
                formatted_key = f"💻 {key.replace('_', ' ').title()}"
            elif "graph" in key.lower():
                formatted_key = f"📊 {key.replace('_', ' ').title()}"
            elif "filter" in key.lower():
                formatted_key = f"🔍 {key.replace('_', ' ').title()}"
            elif "backup" in key.lower():
                formatted_key = f"💾 {key.replace('_', ' ').title()}"
            elif "rollback" in key.lower():
                formatted_key = f"↩️ {key.replace('_', ' ').title()}"
            elif "version" in key.lower():
                formatted_key = f"📋 {key.replace('_', ' ').title()}"
            elif "detail" in key.lower():
                formatted_key = f"🔍 {key.replace('_', ' ').title()}"
            elif "available" in key.lower():
                formatted_key = f"✅ {key.replace('_', ' ').title()}"
            else:
                formatted_key = f"ℹ️ {key.replace('_', ' ').title()}"
            
            formatted_metadata[formatted_key] = value
        
        return formatted_metadata
    
    @staticmethod
    def _format_insights(insights: List[str]) -> List[str]:
        """Format insights with visual enhancements."""
        formatted_insights = []
        
        for insight in insights:
            if "error" in insight.lower() or "fail" in insight.lower():
                formatted_insights.append(f"🚨 {insight}")
            elif "warning" in insight.lower() or "limited" in insight.lower():
                formatted_insights.append(f"⚠️ {insight}")
            elif "success" in insight.lower() or "available" in insight.lower():
                formatted_insights.append(f"✅ {insight}")
            elif "recommend" in insight.lower() or "try" in insight.lower():
                formatted_insights.append(f"💡 {insight}")
            elif "found" in insight.lower() or "discovered" in insight.lower():
                formatted_insights.append(f"🔍 {insight}")
            elif "jarvis" in insight.lower():
                formatted_insights.append(f"🤖 {insight}")
            else:
                formatted_insights.append(f"ℹ️ {insight}")
        
        return formatted_insights
    
    @staticmethod
    def _format_suggestions(suggestions: List[str]) -> List[str]:
        """Format suggestions with visual enhancements."""
        formatted_suggestions = []
        
        for suggestion in suggestions:
            if "check" in suggestion.lower():
                formatted_suggestions.append(f"🔍 {suggestion}")
            elif "install" in suggestion.lower():
                formatted_suggestions.append(f"📦 {suggestion}")
            elif "configure" in suggestion.lower() or "config" in suggestion.lower():
                formatted_suggestions.append(f"⚙️ {suggestion}")
            elif "verify" in suggestion.lower():
                formatted_suggestions.append(f"✅ {suggestion}")
            elif "ensure" in suggestion.lower():
                formatted_suggestions.append(f"🔒 {suggestion}")
            elif "run" in suggestion.lower():
                formatted_suggestions.append(f"🚀 {suggestion}")
            else:
                formatted_suggestions.append(f"💭 {suggestion}")
        
        return formatted_suggestions


def create_beautiful_response(
    operation: str,
    success: bool,
    data: Any = None,
    summary: Optional[Dict] = None,
    metadata: Optional[Dict] = None,
    insights: Optional[List[str]] = None,
    error_message: Optional[str] = None,
    error_type: Optional[str] = None,
    suggestions: Optional[List[str]] = None,
    **kwargs
) -> Dict:
    """
    Create a beautiful response with MCP-compliant format.
    
    Args:
        operation: Name of the operation
        success: Whether the operation was successful
        data: Main data result
        summary: Summary information
        metadata: Additional metadata
        insights: Key insights
        error_message: Error message if failed
        error_type: Error type if failed
        suggestions: Suggestions if failed
        **kwargs: Additional arguments
        
    Returns:
        MCP-compliant response with beautiful formatting
    """
    if success:
        formatted_response = JarvisFormatter.format_success_response(
            operation=operation,
            data=data,
            summary=summary,
            metadata=metadata,
            insights=insights
        )
    else:
        formatted_response = JarvisFormatter.format_error_response(
            operation=operation,
            error_message=error_message or "Unknown error",
            error_type=error_type or "UnknownError",
            suggestions=suggestions
        )
    
    return {
        "content": [{"text": json.dumps(formatted_response, indent=2)}],
        "_meta": {
            "tool": operation,
            "success": success
        },
        "isError": not success
    }