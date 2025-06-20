from typing import Dict, List, Optional
import re

class ContentAnalyzer:
    """Analyzes content to extract information for diagram generation."""

    @staticmethod
    def extract_diagram_info(content: str) -> Dict:
        """Extract information from content to generate appropriate diagrams."""
        diagrams = {}
        
        # Extract architecture/component information
        if architecture_data := ContentAnalyzer._extract_architecture_info(content):
            diagrams['architecture'] = {
                'type': 'component',
                'data': architecture_data
            }
        
        # Extract workflow/process information
        if workflow_data := ContentAnalyzer._extract_workflow_info(content):
            diagrams['workflow'] = {
                'type': 'flowchart',
                'data': workflow_data
            }
        
        # Extract state machine information
        if state_data := ContentAnalyzer._extract_state_info(content):
            diagrams['state_machine'] = {
                'type': 'state',
                'data': state_data
            }
        
        # Extract class structure information
        if class_data := ContentAnalyzer._extract_class_info(content):
            diagrams['class'] = {
                'type': 'class',
                'data': class_data
            }
        
        # Generate comprehensive diagrams if none were extracted
        if not diagrams:
            diagrams = ContentAnalyzer._generate_comprehensive_diagrams(content)
        
        return diagrams

    @staticmethod
    def _generate_comprehensive_diagrams(content: str) -> Dict:
        """Generate comprehensive diagrams covering basic to advanced concepts."""
        diagrams = {}
        
        # Generate a comprehensive architecture diagram
        diagrams['architecture'] = {
            'type': 'component',
            'data': {
                'containers': [
                    {
                        'id': 'client',
                        'name': 'Client Application',
                        'tech': 'Web/Mobile',
                        'desc': 'User-facing application'
                    },
                    {
                        'id': 'api',
                        'name': 'API Gateway',
                        'tech': 'REST/GraphQL',
                        'desc': 'Request routing and authentication'
                    },
                    {
                        'id': 'service',
                        'name': 'Core Service',
                        'tech': 'Backend',
                        'desc': 'Business logic and data processing'
                    },
                    {
                        'id': 'database',
                        'name': 'Database',
                        'tech': 'SQL/NoSQL',
                        'desc': 'Data persistence layer'
                    },
                    {
                        'id': 'cache',
                        'name': 'Cache Layer',
                        'tech': 'Redis/Memcached',
                        'desc': 'Performance optimization'
                    }
                ],
                'components': [
                    {
                        'id': 'auth',
                        'name': 'Authentication Service',
                        'tech': 'JWT/OAuth',
                        'desc': 'User authentication and authorization'
                    },
                    {
                        'id': 'monitoring',
                        'name': 'Monitoring Service',
                        'tech': 'Logging/Metrics',
                        'desc': 'System observability'
                    }
                ],
                'relationships': [
                    {
                        'from': 'client',
                        'to': 'api',
                        'label': 'HTTP requests',
                        'tech': 'REST/HTTPS'
                    },
                    {
                        'from': 'api',
                        'to': 'auth',
                        'label': 'Validate tokens',
                        'tech': 'JWT'
                    },
                    {
                        'from': 'api',
                        'to': 'service',
                        'label': 'Process requests',
                        'tech': 'Internal API'
                    },
                    {
                        'from': 'service',
                        'to': 'database',
                        'label': 'CRUD operations',
                        'tech': 'SQL'
                    },
                    {
                        'from': 'service',
                        'to': 'cache',
                        'label': 'Cache data',
                        'tech': 'Redis'
                    },
                    {
                        'from': 'service',
                        'to': 'monitoring',
                        'label': 'Log events',
                        'tech': 'Metrics'
                    }
                ]
            }
        }
        
        # Generate a comprehensive workflow diagram
        diagrams['workflow'] = {
            'type': 'flowchart',
            'data': {
                'nodes': {
                    'start': {'label': 'Start', 'shape': 'circle'},
                    'input': {'label': 'User Input'},
                    'validate': {'label': 'Validate Input', 'shape': 'diamond'},
                    'process': {'label': 'Process Request'},
                    'auth': {'label': 'Authentication Check', 'shape': 'diamond'},
                    'authorize': {'label': 'Authorization Check', 'shape': 'diamond'},
                    'execute': {'label': 'Execute Business Logic'},
                    'persist': {'label': 'Persist Data'},
                    'cache': {'label': 'Update Cache'},
                    'response': {'label': 'Generate Response'},
                    'log': {'label': 'Log Activity'},
                    'end': {'label': 'End', 'shape': 'circle'}
                },
                'connections': [
                    {'from': 'start', 'to': 'input'},
                    {'from': 'input', 'to': 'validate'},
                    {'from': 'validate', 'to': 'process', 'label': 'Valid'},
                    {'from': 'validate', 'to': 'input', 'label': 'Invalid', 'style': '-.->'},
                    {'from': 'process', 'to': 'auth'},
                    {'from': 'auth', 'to': 'authorize', 'label': 'Authenticated'},
                    {'from': 'auth', 'to': 'response', 'label': 'Unauthorized', 'style': '-.->'},
                    {'from': 'authorize', 'to': 'execute', 'label': 'Authorized'},
                    {'from': 'authorize', 'to': 'response', 'label': 'Forbidden', 'style': '-.->'},
                    {'from': 'execute', 'to': 'persist'},
                    {'from': 'persist', 'to': 'cache'},
                    {'from': 'cache', 'to': 'response'},
                    {'from': 'response', 'to': 'log'},
                    {'from': 'log', 'to': 'end'}
                ]
            }
        }
        
        # Generate a comprehensive state diagram
        diagrams['state_machine'] = {
            'type': 'state',
            'data': {
                'states': [
                    {'name': 'Initialized'},
                    {
                        'name': 'Processing',
                        'composite': True,
                        'substates': [
                            'Validating',
                            'Authenticating',
                            'Executing',
                            'Persisting'
                        ]
                    },
                    {'name': 'Completed'},
                    {'name': 'Failed'},
                    {'name': 'Retrying'}
                ],
                'transitions': [
                    {'from': 'Initialized', 'to': 'Processing', 'label': 'start'},
                    {'from': 'Processing', 'to': 'Completed', 'label': 'success'},
                    {'from': 'Processing', 'to': 'Failed', 'label': 'error'},
                    {'from': 'Failed', 'to': 'Retrying', 'label': 'retry'},
                    {'from': 'Retrying', 'to': 'Processing', 'label': 'restart'},
                    {'from': 'Retrying', 'to': 'Failed', 'label': 'max_retries'},
                    {'from': 'Completed', 'to': 'Initialized', 'label': 'reset'}
                ]
            }
        }
        
        return diagrams

    @staticmethod
    def _extract_architecture_info(content: str) -> Optional[Dict]:
        """Extract system architecture information from content."""
        components = {}
        relationships = []
        
        # Look for component/service descriptions
        component_pattern = r'(?:component|service|module|system)\s+["\']([^"\']+)["\'].*?(?:using|with)\s+([^\n.]+)'
        for match in re.finditer(component_pattern, content, re.IGNORECASE):
            name, tech = match.groups()
            component_id = name.lower().replace(' ', '_')
            components[component_id] = {
                'id': component_id,
                'name': name,
                'tech': tech.strip(),
                'desc': f"{name} using {tech.strip()}"
            }
        
        # Look for relationships/interactions
        relation_pattern = r'([A-Za-z_]+)\s+(?:calls|connects to|uses|interacts with)\s+([A-Za-z_]+)(?:\s+via\s+([^\n.]+))?'
        for match in re.finditer(relation_pattern, content, re.IGNORECASE):
            from_comp, to_comp, tech = match.groups()
            relationships.append({
                'from': from_comp.lower(),
                'to': to_comp.lower(),
                'label': 'uses',
                'tech': tech if tech else 'API'
            })
        
        if components:
            return {
                'containers': list(components.values()),
                'components': [],
                'relationships': relationships
            }
        return None

    @staticmethod
    def _extract_workflow_info(content: str) -> Optional[Dict]:
        """Extract workflow/process information from content."""
        nodes = {}
        connections = []
        
        # Look for steps/stages in processes
        step_pattern = r'(?:step|stage|phase)\s*\d*:?\s*([^\n.]+)'
        steps = re.finditer(step_pattern, content, re.IGNORECASE)
        prev_step_id = None
        
        for i, match in enumerate(steps):
            step_desc = match.group(1).strip()
            step_id = f"step_{i}"
            nodes[step_id] = {
                'label': step_desc,
                'shape': 'rectangle'
            }
            
            if prev_step_id:
                connections.append({
                    'from': prev_step_id,
                    'to': step_id
                })
            prev_step_id = step_id
        
        # Look for conditions/decisions
        condition_pattern = r'if\s+([^\n,]+)(?:\s*,\s*then\s+([^\n.]+))?'
        for match in re.finditer(condition_pattern, content, re.IGNORECASE):
            condition, action = match.groups()
            cond_id = f"cond_{len(nodes)}"
            nodes[cond_id] = {
                'label': condition.strip(),
                'shape': 'diamond'
            }
            
            if action:
                action_id = f"action_{len(nodes)}"
                nodes[action_id] = {
                    'label': action.strip()
                }
                connections.append({
                    'from': cond_id,
                    'to': action_id,
                    'label': 'Yes'
                })
        
        if nodes:
            return {
                'nodes': nodes,
                'connections': connections
            }
        return None

    @staticmethod
    def _extract_state_info(content: str) -> Optional[Dict]:
        """Extract state machine information from content."""
        states = []
        transitions = []
        
        # Look for states and their descriptions
        state_pattern = r'(?:state|status):\s*([^\n.]+)(?:\s*contains\s*([^\n.]+))?'
        for match in re.finditer(state_pattern, content, re.IGNORECASE):
            state_name, substates = match.groups()
            state = {'name': state_name.strip()}
            
            if substates:
                state['composite'] = True
                state['substates'] = [s.strip() for s in substates.split(',')]
            
            states.append(state)
        
        # Look for transitions between states
        transition_pattern = r'(?:when|if)\s+([^\n,]+)\s*,?\s*(?:then)?\s+(?:transition|move|go)\s+(?:from\s+([^\n]+)\s+)?to\s+([^\n.]+)'
        for match in re.finditer(transition_pattern, content, re.IGNORECASE):
            trigger, from_state, to_state = match.groups()
            if from_state:
                transitions.append({
                    'from': from_state.strip(),
                    'to': to_state.strip(),
                    'label': trigger.strip()
                })
        
        if states:
            return {
                'states': states,
                'transitions': transitions
            }
        return None

    @staticmethod
    def _extract_class_info(content: str) -> Optional[Dict]:
        """Extract class structure information from content."""
        classes = {}
        
        # Look for class definitions and their properties
        class_pattern = r'class\s+([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(([^)]+)\))?\s*:([^}]+)'
        for match in re.finditer(class_pattern, content):
            class_name, parent, body = match.groups()
            class_data = {
                'attributes': [],
                'methods': []
            }
            
            # Extract attributes
            attr_pattern = r'(?:self\.)?([A-Za-z_][A-Za-z0-9_]*)\s*(?::\s*([A-Za-z_][A-Za-z0-9_]*))?\s*='
            for attr_match in re.finditer(attr_pattern, body):
                attr_name, attr_type = attr_match.groups()
                class_data['attributes'].append({
                    'name': f"{attr_name}: {attr_type if attr_type else 'Any'}"
                })
            
            # Extract methods
            method_pattern = r'def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*(?:->\s*([A-Za-z_][A-Za-z0-9_]*))?\s*:'
            for method_match in re.finditer(method_pattern, body):
                method_name, params, return_type = method_match.groups()
                class_data['methods'].append({
                    'name': method_name,
                    'params': [p.strip() for p in params.split(',') if p.strip()],
                    'return_type': return_type if return_type else 'None'
                })
            
            classes[class_name] = class_data
        
        if classes:
            return {
                'classes': classes,
                'relationships': []  # Could be enhanced to detect relationships
            }
        return None 