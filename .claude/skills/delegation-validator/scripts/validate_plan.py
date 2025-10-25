#!/usr/bin/env python3
"""
Validates lesson plans against Delegation criteria.

Usage:
    python validate_plan.py --input lesson_plan.md --format json
    python validate_plan.py --input lesson_plan.txt --format text
"""

import argparse
import json
import re
import sys

def analyze_problem_awareness(text):
    """
    Score 0-10 for Problem Awareness coverage.

    Criteria:
    - 0-3: No mention of defining objectives
    - 4-6: Mentions objectives but assumes AI use
    - 7-9: Teaches when to use AI vs when not to
    - 10: Includes modalities (Automation/Augmentation/Agency)
    """
    score = 0
    text_lower = text.lower()

    # Check for objective-setting keywords (3 points)
    objective_keywords = [
        'objetivo', 'goal', 'problema', 'problem', 'propósito', 'purpose',
        'o que estou tentando', 'what am i trying', 'definir meta', 'define goal'
    ]
    if any(kw in text_lower for kw in objective_keywords):
        score += 3

    # Check for questioning IF should use AI (3 points)
    questioning_keywords = [
        'quando usar', 'when to use', 'se deve', 'whether to',
        'deveria usar', 'should use', 'é adequado', 'is appropriate',
        'quando não usar', 'when not to'
    ]
    if any(kw in text_lower for kw in questioning_keywords):
        score += 3

    # Check for interaction modalities (4 points)
    modalities = [
        'automação', 'automation', 'aumento', 'augmentation',
        'ampliação', 'agência', 'agency'
    ]
    modality_count = sum(1 for mod in modalities if mod in text_lower)
    if modality_count >= 2:
        score += 4
    elif modality_count == 1:
        score += 2

    return min(score, 10)


def analyze_platform_awareness(text):
    """
    Score 0-10 for Platform Awareness coverage.

    Criteria:
    - 0-3: Assumes one AI tool
    - 4-6: Mentions multiple tools but doesn't compare
    - 7-9: Teaches comparison of capabilities AND limitations
    - 10: Includes ethical/privacy considerations
    """
    score = 0
    text_lower = text.lower()

    # Count AI tools mentioned (up to 4 points)
    tools = [
        'chatgpt', 'claude', 'gemini', 'copilot', 'midjourney',
        'dall-e', 'perplexity', 'bard', 'gpt', 'llama'
    ]
    tools_count = sum(1 for tool in tools if tool in text_lower)

    if tools_count >= 1:
        score += 1
    if tools_count >= 3:
        score += 3

    # Check for comparison discussion (3 points)
    comparison_keywords = [
        'compar', 'diferença', 'difference', 'versus', 'vs',
        'melhor para', 'better for', 'adequado para', 'suitable for'
    ]
    if any(kw in text_lower for kw in comparison_keywords):
        score += 2

    # Check for limitations discussion (3 points)
    limitations_keywords = [
        'limitações', 'limitations', 'não pode', 'cannot',
        'problemas', 'issues', 'desvantagens', 'disadvantages',
        'fraquezas', 'weaknesses'
    ]
    if any(kw in text_lower for kw in limitations_keywords):
        score += 3

    # Check for ethical considerations (2 points)
    ethical_keywords = [
        'privacidade', 'privacy', 'ética', 'ethics',
        'viés', 'bias', 'transparência', 'transparency',
        'responsabilidade', 'responsibility', 'segurança', 'security'
    ]
    if any(kw in text_lower for kw in ethical_keywords):
        score += 2

    return min(score, 10)


def analyze_task_delegation(text):
    """
    Score 0-10 for Task Delegation coverage.

    Criteria:
    - 0-3: No guidance on dividing work
    - 4-6: Generic advice on "use AI for X"
    - 7-9: Specific strategies for human-AI collaboration
    - 10: Includes examples of good vs bad delegation + justifications
    """
    score = 0
    text_lower = text.lower()

    # Check for division of work discussion (3 points)
    division_keywords = [
        'dividir', 'divide', 'separar', 'split',
        'humano.*ia', 'human.*ai', 'ia.*humano', 'ai.*human',
        'o que.*ia faz', 'what.*ai does', 'o que.*humano faz', 'what.*human does'
    ]
    if any(re.search(kw, text_lower) for kw in division_keywords):
        score += 3

    # Check for strategies mentioned (3 points)
    strategies = [
        'ia primeiro', 'ai first', 'humano primeiro', 'human first',
        'colabor', 'iterativ', 'incremental', 'refin',
        'orquestra', 'coordinat'
    ]
    strategy_count = sum(1 for strat in strategies if strat in text_lower)
    if strategy_count >= 2:
        score += 3
    elif strategy_count == 1:
        score += 2

    # Check for examples of good vs bad delegation (2 points)
    example_keywords = [
        'exemplo', 'example', 'bom.*ruim', 'good.*bad',
        'adequado.*inadequado', 'appropriate.*inappropriate',
        'efetiv.*inefetiv', 'effective.*ineffective'
    ]
    if any(re.search(kw, text_lower) for kw in example_keywords):
        score += 2

    # Check for justifications (2 points)
    justification_keywords = [
        'justific', 'porque', 'why', 'razão', 'reason',
        'motivo', 'rationale', 'por que', 'explicação', 'explanation'
    ]
    if any(kw in text_lower for kw in justification_keywords):
        score += 2

    return min(score, 10)


def identify_gaps(scores):
    """Identify specific gaps based on scores."""
    gaps = []

    if scores['problem_awareness'] < 7:
        gaps.append({
            'category': 'Problem Awareness',
            'issue': 'Lesson should teach students to question IF they should use AI, not just assume AI use',
            'severity': 'high' if scores['problem_awareness'] < 4 else 'medium'
        })

    if scores['platform_awareness'] < 7:
        gaps.append({
            'category': 'Platform Awareness',
            'issue': 'Lesson should compare multiple AI tools including their limitations',
            'severity': 'high' if scores['platform_awareness'] < 4 else 'medium'
        })

    if scores['task_delegation'] < 7:
        gaps.append({
            'category': 'Task Delegation',
            'issue': 'Lesson should provide specific strategies for dividing work between human and AI',
            'severity': 'high' if scores['task_delegation'] < 4 else 'medium'
        })

    return gaps


def generate_recommendations(scores):
    """Generate actionable recommendations based on scores."""
    recommendations = []

    # Problem Awareness recommendations
    if scores['problem_awareness'] < 10:
        if scores['problem_awareness'] < 7:
            recommendations.append({
                'category': 'Problem Awareness',
                'action': 'Add decision framework: Teach students to ask "Should I use AI for this task?" before diving into "how"',
                'priority': 'high'
            })
        if scores['problem_awareness'] < 10:
            recommendations.append({
                'category': 'Problem Awareness',
                'action': 'Add exercise: Students identify which interaction mode (Automation/Augmentation/Agency) fits different tasks',
                'priority': 'medium'
            })

    # Platform Awareness recommendations
    if scores['platform_awareness'] < 10:
        if scores['platform_awareness'] < 7:
            recommendations.append({
                'category': 'Platform Awareness',
                'action': 'Add comparison activity: Students test 2-3 AI tools on same task and compare capabilities/limitations',
                'priority': 'high'
            })
        if scores['platform_awareness'] < 10:
            recommendations.append({
                'category': 'Platform Awareness',
                'action': 'Include discussion on privacy/ethical considerations when choosing AI tools',
                'priority': 'medium'
            })

    # Task Delegation recommendations
    if scores['task_delegation'] < 10:
        if scores['task_delegation'] < 7:
            recommendations.append({
                'category': 'Task Delegation',
                'action': 'Add workflow diagram: Show specific strategies for dividing work (AI first, human first, iterative)',
                'priority': 'high'
            })
        if scores['task_delegation'] < 10:
            recommendations.append({
                'category': 'Task Delegation',
                'action': 'Add examples: Show good delegation vs bad delegation with justifications for each',
                'priority': 'medium'
            })

    return recommendations


def validate_lesson_plan(text):
    """Main validation function."""
    scores = {
        'problem_awareness': analyze_problem_awareness(text),
        'platform_awareness': analyze_platform_awareness(text),
        'task_delegation': analyze_task_delegation(text)
    }

    scores['overall'] = round(sum(scores.values()) / 3, 1)

    gaps = identify_gaps(scores)
    recommendations = generate_recommendations(scores)

    return {
        'scores': scores,
        'gaps': gaps,
        'recommendations': recommendations
    }


def format_text_output(result):
    """Format result as human-readable text."""
    output = []

    # Scores
    output.append("=== DELEGATION VALIDATOR RESULTS ===\n")
    output.append(f"Problem Awareness:  {result['scores']['problem_awareness']}/10")
    output.append(f"Platform Awareness: {result['scores']['platform_awareness']}/10")
    output.append(f"Task Delegation:    {result['scores']['task_delegation']}/10")
    output.append(f"Overall Score:      {result['scores']['overall']}/10\n")

    # Classification
    overall = result['scores']['overall']
    if overall >= 8:
        classification = "EXCELLENT - Ready to pilot"
    elif overall >= 6:
        classification = "GOOD - Minor improvements needed"
    elif overall >= 4:
        classification = "ADEQUATE - Significant gaps to address"
    else:
        classification = "NEEDS WORK - Major revision required"

    output.append(f"Classification: {classification}\n")

    # Gaps
    if result['gaps']:
        output.append(f"=== GAPS IDENTIFIED ({len(result['gaps'])}) ===")
        for i, gap in enumerate(result['gaps'], 1):
            output.append(f"\n{i}. [{gap['severity'].upper()}] {gap['category']}")
            output.append(f"   {gap['issue']}")
    else:
        output.append("=== NO SIGNIFICANT GAPS ===")
        output.append("Lesson plan covers all Delegation subcategories adequately.\n")

    # Recommendations
    if result['recommendations']:
        output.append(f"\n=== RECOMMENDATIONS ({len(result['recommendations'])}) ===")
        high_priority = [r for r in result['recommendations'] if r['priority'] == 'high']
        medium_priority = [r for r in result['recommendations'] if r['priority'] == 'medium']

        if high_priority:
            output.append("\nHigh Priority:")
            for i, rec in enumerate(high_priority, 1):
                output.append(f"{i}. [{rec['category']}] {rec['action']}")

        if medium_priority:
            output.append("\nMedium Priority:")
            for i, rec in enumerate(medium_priority, 1):
                output.append(f"{i}. [{rec['category']}] {rec['action']}")

    return '\n'.join(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Validate Delegation lesson plan coverage',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python validate_plan.py --input lesson_plan.md --format json
  python validate_plan.py --input lesson_plan.txt --format text
        '''
    )
    parser.add_argument('--input', required=True, help='Lesson plan file path')
    parser.add_argument('--format', default='text', choices=['json', 'text'],
                        help='Output format (default: text)')

    args = parser.parse_args()

    try:
        # Read lesson plan
        with open(args.input, 'r', encoding='utf-8') as f:
            lesson_text = f.read()

        # Validate
        result = validate_lesson_plan(lesson_text)

        # Output
        if args.format == 'json':
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_text_output(result))

    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
