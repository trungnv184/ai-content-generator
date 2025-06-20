from typing import Dict, List

class DiagramGenerator:
    """Utility class for generating technical diagrams using Mermaid syntax."""

    @staticmethod
    def generate_diagram(diagram_type: str, diagram_data: Dict) -> str:
        """Generate technical diagrams based on the type and data provided."""
        if diagram_type == "flowchart":
            return DiagramGenerator._generate_flowchart(diagram_data)
        elif diagram_type == "class":
            return DiagramGenerator._generate_class_diagram(diagram_data)
        elif diagram_type == "component":
            return DiagramGenerator._generate_component_diagram(diagram_data)
        elif diagram_type == "state":
            return DiagramGenerator._generate_state_diagram(diagram_data)
        else:
            raise ValueError(f"Unsupported diagram type: {diagram_type}")

    @staticmethod
    def _generate_flowchart(data: Dict) -> str:
        """Generate a flowchart diagram using Mermaid."""
        diagram = """```mermaid
flowchart TD
"""
        # Add nodes
        for node_id, node_data in data.get('nodes', {}).items():
            shape = node_data.get('shape', '[]')  # Default to rectangle
            if shape == 'circle':
                diagram += f'    {node_id}(("{node_data["label"]}"))\n'
            elif shape == 'diamond':
                diagram += f'    {node_id}{{{node_data["label"]}}}\n'
            else:
                diagram += f'    {node_id}["{node_data["label"]}"]\n'

        # Add connections
        for conn in data.get('connections', []):
            style = conn.get('style', '-->')  # Default to normal arrow
            label = conn.get('label', '')
            if label:
                diagram += f'    {conn["from"]} {style}|{label}| {conn["to"]}\n'
            else:
                diagram += f'    {conn["from"]} {style} {conn["to"]}\n'

        diagram += "```"
        return diagram

    @staticmethod
    def _generate_class_diagram(data: Dict) -> str:
        """Generate a class diagram using Mermaid."""
        diagram = """```mermaid
classDiagram
"""
        # Add classes
        for class_name, class_data in data.get('classes', {}).items():
            diagram += f'    class {class_name} {{\n'
            
            # Add attributes
            for attr in class_data.get('attributes', []):
                visibility = attr.get('visibility', '+')  # Default to public
                diagram += f'        {visibility}{attr["name"]}\n'
            
            # Add methods
            for method in class_data.get('methods', []):
                visibility = method.get('visibility', '+')
                params = ', '.join(method.get('params', []))
                return_type = method.get('return_type', '')
                if return_type:
                    diagram += f'        {visibility}{method["name"]}({params}) {return_type}\n'
                else:
                    diagram += f'        {visibility}{method["name"]}({params})\n'
            
            diagram += '    }\n'

        # Add relationships
        for rel in data.get('relationships', []):
            diagram += f'    {rel["from"]} {rel["type"]} {rel["to"]}\n'

        diagram += "```"
        return diagram

    @staticmethod
    def _generate_component_diagram(data: Dict) -> str:
        """Generate a component diagram using Mermaid."""
        diagram = """```mermaid
C4Component
"""
        # Add containers
        for container in data.get('containers', []):
            diagram += f'    Container({container["id"]}, "{container["name"]}", "{container["tech"]}", "{container["desc"]}")\n'

        # Add components
        for component in data.get('components', []):
            diagram += f'    Component({component["id"]}, "{component["name"]}", "{component["tech"]}", "{component["desc"]}")\n'

        # Add relationships
        for rel in data.get('relationships', []):
            diagram += f'    Rel({rel["from"]}, {rel["to"]}, "{rel["label"]}", "{rel["tech"]}")\n'

        diagram += "```"
        return diagram

    @staticmethod
    def _generate_state_diagram(data: Dict) -> str:
        """Generate a state diagram using Mermaid."""
        diagram = """```mermaid
stateDiagram-v2
"""
        # Add states
        for state in data.get('states', []):
            if state.get('composite', False):
                diagram += f'    state {state["name"]} {{\n'
                for sub_state in state.get('substates', []):
                    diagram += f'        {sub_state}\n'
                diagram += '    }\n'
            else:
                diagram += f'    {state["name"]}\n'

        # Add transitions
        for trans in data.get('transitions', []):
            label = trans.get('label', '')
            if label:
                diagram += f'    {trans["from"]} --> {trans["to"]}: {label}\n'
            else:
                diagram += f'    {trans["from"]} --> {trans["to"]}\n'

        diagram += "```"
        return diagram 