import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DetectionMethod(str, Enum):
    DOMAIN_MATCH = "domain_match"
    KEYWORD_MATCH = "keyword_match"
    PROCESS_MATCH = "process_match"
    VISUAL_PATTERN = "visual_pattern"
    BEHAVIORAL = "behavioral"


class AIToolDetector:
    """
    Detects AI tool usage based on multiple signals.
    """

    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path("config/ai_tools.json")

        self.config_path = config_path
        self.tools = self._load_config()

    def _load_config(self) -> List[Dict]:
        """Load AI tools configuration"""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return data.get('tools', [])
        except FileNotFoundError:
            print(f"Warning: AI tools config not found at {self.config_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"Error parsing AI tools config: {e}")
            return []

    def reload_config(self):
        """Reload configuration from file"""
        self.tools = self._load_config()

    def detect_from_domain(self, domain: str) -> List[Dict]:
        """
        Detect AI tools based on domain.

        Args:
            domain: Domain name (e.g., "chatgpt.com")

        Returns:
            List of detection results
        """
        detections = []

        for tool in self.tools:
            if not tool.get('enabled', True):
                continue

            domains = tool.get('detection_methods', {}).get('domains', [])

            for tool_domain in domains:
                if tool_domain.lower() in domain.lower() or domain.lower() in tool_domain.lower():
                    detections.append({
                        'tool_name': tool['name'],
                        'tool_type': tool['type'],
                        'detection_method': DetectionMethod.DOMAIN_MATCH,
                        'confidence_score': 0.9,  # High confidence for domain matches
                        'confidence_level': ConfidenceLevel.HIGH,
                        'matched_value': domain,
                        'priority': tool.get('priority', 50),
                    })

        return detections

    def detect_from_keywords(self, text: str) -> List[Dict]:
        """
        Detect AI tools based on keywords in text.

        Args:
            text: Text to analyze (from OCR or other source)

        Returns:
            List of detection results
        """
        detections = []
        text_lower = text.lower()

        for tool in self.tools:
            if not tool.get('enabled', True):
                continue

            keywords = tool.get('detection_methods', {}).get('keywords', [])
            matched_keywords = []

            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matched_keywords.append(keyword)

            if matched_keywords:
                # More keywords = higher confidence
                confidence = min(0.3 + (len(matched_keywords) * 0.15), 0.8)

                detections.append({
                    'tool_name': tool['name'],
                    'tool_type': tool['type'],
                    'detection_method': DetectionMethod.KEYWORD_MATCH,
                    'confidence_score': confidence,
                    'confidence_level': self._score_to_level(confidence),
                    'matched_value': ', '.join(matched_keywords),
                    'priority': tool.get('priority', 50),
                })

        return detections

    def detect_from_process(self, process_name: str) -> List[Dict]:
        """
        Detect AI tools based on process name.

        Args:
            process_name: Process/application name

        Returns:
            List of detection results
        """
        detections = []
        process_lower = process_name.lower()

        for tool in self.tools:
            if not tool.get('enabled', True):
                continue

            processes = tool.get('detection_methods', {}).get('processes', [])

            for tool_process in processes:
                if tool_process.lower() in process_lower:
                    detections.append({
                        'tool_name': tool['name'],
                        'tool_type': tool['type'],
                        'detection_method': DetectionMethod.PROCESS_MATCH,
                        'confidence_score': 0.95,  # Very high for process matches
                        'confidence_level': ConfidenceLevel.VERY_HIGH,
                        'matched_value': process_name,
                        'priority': tool.get('priority', 50),
                    })

        return detections

    def detect_from_window_title(self, window_title: str) -> List[Dict]:
        """
        Detect AI tools from window title.

        Args:
            window_title: Window title text

        Returns:
            List of detection results
        """
        # Check keywords in window title
        return self.detect_from_keywords(window_title)

    def analyze_screenshot_context(
        self,
        ocr_text: str,
        window_title: str,
        process_name: str,
        domain: Optional[str] = None
    ) -> List[Dict]:
        """
        Analyze multiple signals to detect AI tool usage.

        Args:
            ocr_text: Text extracted from screenshot
            window_title: Active window title
            process_name: Process name
            domain: Browser domain (if applicable)

        Returns:
            Consolidated detection results
        """
        all_detections = []

        # Domain detection (highest priority)
        if domain:
            all_detections.extend(self.detect_from_domain(domain))

        # Process detection
        all_detections.extend(self.detect_from_process(process_name))

        # Window title detection
        all_detections.extend(self.detect_from_window_title(window_title))

        # OCR text detection
        all_detections.extend(self.detect_from_keywords(ocr_text))

        # Deduplicate and combine evidence
        return self._consolidate_detections(all_detections)

    def _consolidate_detections(self, detections: List[Dict]) -> List[Dict]:
        """
        Consolidate multiple detections of the same tool.
        """
        if not detections:
            return []

        # Group by tool name
        tools_map = {}
        for detection in detections:
            tool_name = detection['tool_name']

            if tool_name not in tools_map:
                tools_map[tool_name] = {
                    'tool_name': tool_name,
                    'tool_type': detection['tool_type'],
                    'detection_methods': [],
                    'matched_values': [],
                    'confidence_scores': [],
                    'priority': detection['priority'],
                }

            tools_map[tool_name]['detection_methods'].append(detection['detection_method'])
            tools_map[tool_name]['matched_values'].append(detection['matched_value'])
            tools_map[tool_name]['confidence_scores'].append(detection['confidence_score'])

        # Calculate combined confidence
        consolidated = []
        for tool_name, data in tools_map.items():
            # Multiple detection methods increase confidence
            num_methods = len(set(data['detection_methods']))
            avg_confidence = sum(data['confidence_scores']) / len(data['confidence_scores'])

            # Boost confidence based on number of different detection methods
            combined_confidence = min(avg_confidence * (1 + num_methods * 0.1), 1.0)

            consolidated.append({
                'tool_name': tool_name,
                'tool_type': data['tool_type'],
                'detection_methods': list(set(data['detection_methods'])),
                'matched_values': data['matched_values'],
                'confidence_score': round(combined_confidence, 4),
                'confidence_level': self._score_to_level(combined_confidence),
                'priority': data['priority'],
                'num_signals': len(data['confidence_scores']),
            })

        # Sort by priority and confidence
        consolidated.sort(key=lambda x: (x['priority'], x['confidence_score']), reverse=True)

        return consolidated

    def _score_to_level(self, score: float) -> ConfidenceLevel:
        """Convert confidence score to level"""
        if score >= 0.8:
            return ConfidenceLevel.VERY_HIGH
        elif score >= 0.6:
            return ConfidenceLevel.HIGH
        elif score >= 0.3:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def get_enabled_tools(self) -> List[Dict]:
        """Get list of enabled AI tools"""
        return [tool for tool in self.tools if tool.get('enabled', True)]

    def get_tool_by_name(self, name: str) -> Optional[Dict]:
        """Get tool configuration by name"""
        for tool in self.tools:
            if tool['name'].lower() == name.lower():
                return tool
        return None
