"""
Generate SVG neural network diagrams directly from LaTeX TikZ source code.
Converts Module 12 LaTeX diagrams to web-native SVG format.
"""

def generate_perceptron_svg():
    """
    Perceptron diagram from LaTeX (lines 206-245)
    Shows: inputs -> weights -> summation -> activation -> output
    """
    svg = '''<svg viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 850px; height: auto;">
    <defs>
        <style>
            .input-node { fill: #F44336; stroke: #8B0000; stroke-width: 2; }
            .bias-node { fill: #FFC107; stroke: #FFB300; stroke-width: 2; }
            .computation-box { fill: #E8F5E9; stroke: #2D6A4F; stroke-width: 2; }
            .activation-box { fill: #FFF9C4; stroke: #F57F17; stroke-width: 2; }
            .output-node { fill: #4CAF50; stroke: #1B5E20; stroke-width: 2; }
            .connection { stroke: #333; stroke-width: 2; fill: none; }
            .flow { stroke: #0047B2; stroke-width: 2.5; fill: none; }
            .label { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }
            .weight-label { font-family: Arial, sans-serif; font-size: 13px; fill: #C62828; font-weight: bold; }
        </style>
    </defs>

    <!-- Input neurons (x1, x2, x3) -->
    <circle cx="80" cy="80" r="18" class="input-node"/>
    <text x="80" y="87" text-anchor="middle" fill="white" font-size="16" font-weight="bold">x₁</text>

    <circle cx="80" cy="160" r="18" class="input-node"/>
    <text x="80" y="167" text-anchor="middle" fill="white" font-size="16" font-weight="bold">x₂</text>

    <circle cx="80" cy="240" r="18" class="input-node"/>
    <text x="80" y="247" text-anchor="middle" fill="white" font-size="16" font-weight="bold">x₃</text>

    <!-- Bias neuron (x0/b) -->
    <circle cx="80" cy="300" r="18" class="bias-node"/>
    <text x="80" y="307" text-anchor="middle" fill="white" font-size="16" font-weight="bold">x₀</text>

    <!-- Input labels -->
    <text x="30" y="87" text-anchor="end" class="label" font-size="12">Inputs</text>

    <!-- Connections from inputs to summation -->
    <line x1="98" y1="80" x2="240" y2="130" class="connection"/>
    <line x1="98" y1="160" x2="240" y2="160" class="connection"/>
    <line x1="98" y1="240" x2="240" y2="190" class="connection"/>
    <line x1="98" y1="300" x2="240" y2="210" class="connection"/>

    <!-- Weight labels -->
    <text x="150" y="100" class="weight-label">w₁</text>
    <text x="160" y="155" class="weight-label">w₂</text>
    <text x="150" y="220" class="weight-label">w₃</text>
    <text x="155" y="260" class="weight-label">b</text>

    <!-- Summation node -->
    <rect x="240" y="110" width="90" height="90" rx="8" class="computation-box"/>
    <text x="285" y="165" text-anchor="middle" fill="#2D6A4F" font-size="48" font-weight="bold">Σ</text>

    <!-- Flow arrow: summation to activation -->
    <line x1="330" y1="155" x2="420" y2="155" class="flow"/>
    <text x="375" y="145" class="label" font-size="11">z = Σwᵢxᵢ + b</text>

    <!-- Activation function node -->
    <rect x="420" y="110" width="90" height="90" rx="8" class="activation-box"/>
    <text x="465" y="165" text-anchor="middle" fill="#F57F17" font-size="48" font-weight="bold">σ</text>

    <!-- Flow arrow: activation to output -->
    <line x1="510" y1="155" x2="600" y2="155" class="flow"/>
    <text x="545" y="145" class="label" font-size="11">y = σ(z)</text>

    <!-- Output neuron -->
    <circle cx="630" cy="155" r="22" class="output-node"/>
    <text x="630" y="163" text-anchor="middle" fill="white" font-size="16" font-weight="bold">y</text>

    <!-- Output label -->
    <text x="680" y="163" class="label" font-size="12">Output</text>

    <!-- Mathematical formulation box -->
    <rect x="50" y="260" width="800" height="70" rx="6" fill="#F5F5F5" stroke="#CCC" stroke-width="1"/>
    <text x="70" y="285" font-weight="bold" font-size="13" fill="#333">Mathematical Model:</text>
    <text x="70" y="310" font-size="12" fill="#555">z = Σᵢ wᵢxᵢ + b = w^T x + b</text>
    <text x="70" y="330" font-size="12" fill="#555">y = σ(z) = σ(w^T x + b)</text>
</svg>'''
    return svg


def generate_computational_graph_svg():
    """
    Computational graph from LaTeX (lines 1205-1258)
    Shows: x, w → × → z₁ → + → z₂ → σ → y → L with forward and backward passes
    """
    svg = '''<svg viewBox="0 0 1300 280" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 1200px; height: auto;">
    <defs>
        <style>
            .input-node { fill: #FFE0E0; stroke: #C62828; stroke-width: 2; }
            .bias-node { fill: #FFF9C4; stroke: #F57F17; stroke-width: 2; }
            .operation-box { fill: #E3F2FD; stroke: #1976D2; stroke-width: 2; }
            .intermediate-node { fill: #E8F5E9; stroke: #2D6A4F; stroke-width: 2; }
            .output-node { fill: #E8F5E9; stroke: #2D6A4F; stroke-width: 2; }
            .loss-box { fill: #E3F2FD; stroke: #1976D2; stroke-width: 2; }
            .forward-arrow { stroke: #0047B2; stroke-width: 2; fill: none; }
            .backward-arrow { stroke: #D32F2F; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }
            .label { font-family: Arial, sans-serif; font-size: 12px; fill: #333; }
            .grad-label { font-family: Arial, sans-serif; font-size: 10px; fill: #D32F2F; font-weight: bold; }
        </style>
    </defs>

    <!-- Input Nodes -->
    <circle cx="60" cy="100" r="18" class="input-node"/>
    <text x="60" y="107" text-anchor="middle" fill="#C62828" font-size="14" font-weight="bold">x</text>
    <text x="60" y="135" text-anchor="middle" class="label" font-size="11">input</text>

    <circle cx="60" cy="200" r="18" class="input-node"/>
    <text x="60" y="207" text-anchor="middle" fill="#C62828" font-size="14" font-weight="bold">w</text>
    <text x="60" y="228" text-anchor="middle" class="label" font-size="11">weight</text>

    <circle cx="200" cy="200" r="18" class="bias-node"/>
    <text x="200" y="207" text-anchor="middle" fill="#F57F17" font-size="14" font-weight="bold">b</text>
    <text x="200" y="228" text-anchor="middle" class="label" font-size="11">bias</text>

    <!-- Operation 1: Multiplication -->
    <line x1="78" y1="100" x2="270" y2="140" class="forward-arrow"/>
    <line x1="78" y1="200" x2="270" y2="140" class="forward-arrow"/>
    <rect x="270" y="120" width="50" height="40" rx="5" class="operation-box"/>
    <text x="295" y="145" text-anchor="middle" fill="#1976D2" font-size="20" font-weight="bold">×</text>
    <line x1="320" y1="140" x2="370" y2="140" class="forward-arrow"/>
    <text x="340" y="130" class="label" font-size="11">z₁=wx</text>

    <!-- z1 Intermediate Node -->
    <circle cx="390" cy="140" r="16" class="intermediate-node"/>
    <text x="390" y="147" text-anchor="middle" fill="#2D6A4F" font-size="13" font-weight="bold">z₁</text>

    <!-- Operation 2: Addition -->
    <line x1="406" y1="140" x2="460" y2="140" class="forward-arrow"/>
    <line x1="218" y1="200" x2="460" y2="160" class="forward-arrow"/>
    <rect x="460" y="120" width="50" height="40" rx="5" class="operation-box"/>
    <text x="485" y="145" text-anchor="middle" fill="#1976D2" font-size="20" font-weight="bold">+</text>
    <line x1="510" y1="140" x2="560" y2="140" class="forward-arrow"/>
    <text x="530" y="130" class="label" font-size="11">z₂=z₁+b</text>

    <!-- z2 Intermediate Node -->
    <circle cx="580" cy="140" r="16" class="intermediate-node"/>
    <text x="580" y="147" text-anchor="middle" fill="#2D6A4F" font-size="13" font-weight="bold">z₂</text>

    <!-- Operation 3: Activation -->
    <line x1="596" y1="140" x2="650" y2="140" class="forward-arrow"/>
    <rect x="650" y="120" width="50" height="40" rx="5" class="operation-box"/>
    <text x="675" y="145" text-anchor="middle" fill="#1976D2" font-size="20" font-weight="bold">σ</text>
    <line x1="700" y1="140" x2="750" y2="140" class="forward-arrow"/>
    <text x="720" y="130" class="label" font-size="11">y=σ(z₂)</text>

    <!-- Output Node y -->
    <circle cx="770" cy="140" r="16" class="output-node"/>
    <text x="770" y="147" text-anchor="middle" fill="#2D6A4F" font-size="13" font-weight="bold">y</text>

    <!-- Loss Function -->
    <line x1="786" y1="140" x2="840" y2="140" class="forward-arrow"/>
    <rect x="840" y="120" width="50" height="40" rx="5" class="loss-box"/>
    <text x="865" y="145" text-anchor="middle" fill="#1976D2" font-size="18" font-weight="bold">L</text>

    <!-- BACKWARD PASS (Gradients) -->
    <!-- Backward arrows (dashed red) -->
    <path d="M 880 130 Q 860 80 800 80" class="backward-arrow"/>
    <path d="M 730 130 Q 710 80 650 80" class="backward-arrow"/>
    <path d="M 640 130 Q 620 80 560 80" class="backward-arrow"/>
    <path d="M 550 130 Q 530 80 460 80" class="backward-arrow"/>
    <path d="M 510 130 Q 480 80 390 80" class="backward-arrow"/>
    <path d="M 370 150 Q 350 220 280 220" class="backward-arrow"/>
    <path d="M 290 150 Q 270 220 180 220" class="backward-arrow"/>

    <!-- Gradient labels -->
    <text x="850" y="65" class="grad-label">∂L/∂y</text>
    <text x="710" y="65" class="grad-label">∂L/∂z₂</text>
    <text x="560" y="65" class="grad-label">∂L/∂z₁</text>
    <text x="430" y="65" class="grad-label">∂L/∂w</text>
    <text x="350" y="65" class="grad-label">∂L/∂x</text>
    <text x="250" y="240" class="grad-label">∂L/∂b</text>

    <!-- Legend -->
    <rect x="50" y="250" width="1100" height="25" rx="4" fill="#FAFAFA" stroke="#DDD" stroke-width="1"/>
    <text x="70" y="267" font-weight="bold" font-size="11" fill="#333">Forward Pass:</text>
    <line x1="190" x2="220" y1="262" y2="262" class="forward-arrow"/>
    <text x="230" y="267" font-size="10" fill="#666">solid blue arrows</text>
    <text x="500" y="267" font-weight="bold" font-size="11" fill="#D32F2F">Backward Pass (Gradients):</text>
    <line x1="680" x2="710" y1="262" y2="262" class="backward-arrow"/>
    <text x="720" y="267" font-size="10" fill="#666">dashed red arrows</text>
</svg>'''
    return svg


def generate_backpropagation_svg():
    """
    Backpropagation error flow from LaTeX (lines 1043-1094)
    Shows: forward pass (faded) and backward error propagation (bold red)
    """
    svg = '''<svg viewBox="0 0 1000 380" xmlns="http://www.w3.org/2000/svg" style="width: 100%; max-width: 950px; height: auto;">
    <defs>
        <style>
            .input-node { fill: #F44336; stroke: #8B0000; stroke-width: 2; }
            .hidden-node { fill: #2196F3; stroke: #0D47A1; stroke-width: 2; }
            .output-node { fill: #4CAF50; stroke: #1B5E20; stroke-width: 2; }
            .loss-box { fill: #E3F2FD; stroke: #1976D2; stroke-width: 2; }
            .gradient-node { fill: #E8F5E9; stroke: #2D6A4F; stroke-width: 2; }
            .forward-arrow-faded { stroke: #333; stroke-width: 1.5; opacity: 0.2; fill: none; }
            .error-arrow { stroke: #D32F2F; stroke-width: 3; fill: none; }
            .gradient-arrow { stroke: #FF8A33; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }
            .label { font-family: Arial, sans-serif; font-size: 12px; fill: #333; }
            .grad-label { font-family: Arial, sans-serif; font-size: 10px; fill: #D32F2F; font-weight: bold; }
        </style>
    </defs>

    <!-- Forward Pass (Light/Faded) -->
    <!-- Input Layer -->
    <circle cx="80" cy="100" r="16" class="input-node" opacity="0.4"/>
    <text x="80" y="107" text-anchor="middle" fill="white" font-size="12" opacity="0.4">x₁</text>

    <circle cx="80" cy="180" r="16" class="input-node" opacity="0.4"/>
    <text x="80" y="187" text-anchor="middle" fill="white" font-size="12" opacity="0.4">x₂</text>

    <circle cx="80" cy="260" r="16" class="input-node" opacity="0.4"/>
    <text x="80" y="267" text-anchor="middle" fill="white" font-size="12" opacity="0.4">x₃</text>

    <!-- Hidden Layer -->
    <circle cx="380" cy="120" r="16" class="hidden-node" opacity="0.4"/>
    <text x="380" y="127" text-anchor="middle" fill="white" font-size="12" opacity="0.4">h₁</text>

    <circle cx="380" cy="220" r="16" class="hidden-node" opacity="0.4"/>
    <text x="380" y="227" text-anchor="middle" fill="white" font-size="12" opacity="0.4">h₂</text>

    <!-- Output Layer -->
    <circle cx="680" cy="170" r="16" class="output-node" opacity="0.4"/>
    <text x="680" y="177" text-anchor="middle" fill="white" font-size="12" opacity="0.4">y</text>

    <!-- Loss Function -->
    <rect x="750" y="154" width="50" height="32" rx="4" class="loss-box" opacity="0.4"/>
    <text x="775" y="174" text-anchor="middle" fill="#1976D2" font-size="14" opacity="0.4">L</text>

    <!-- Forward connections (light) -->
    <line x1="96" y1="100" x2="364" y2="120" class="forward-arrow-faded"/>
    <line x1="96" y1="100" x2="364" y2="220" class="forward-arrow-faded"/>
    <line x1="96" y1="180" x2="364" y2="120" class="forward-arrow-faded"/>
    <line x1="96" y1="180" x2="364" y2="220" class="forward-arrow-faded"/>
    <line x1="96" y1="260" x2="364" y2="120" class="forward-arrow-faded"/>
    <line x1="96" y1="260" x2="364" y2="220" class="forward-arrow-faded"/>
    <line x1="396" y1="120" x2="664" y2="170" class="forward-arrow-faded"/>
    <line x1="396" y1="220" x2="664" y2="170" class="forward-arrow-faded"/>
    <line x1="696" y1="170" x2="750" y2="170" class="forward-arrow-faded"/>

    <!-- Layer Labels -->
    <text x="80" y="310" text-anchor="middle" class="label" font-weight="bold">Input</text>
    <text x="380" y="310" text-anchor="middle" class="label" font-weight="bold">Hidden</text>
    <text x="680" y="310" text-anchor="middle" class="label" font-weight="bold">Output</text>

    <!-- BACKWARD ERROR FLOW (Bold Red Arrows) -->
    <!-- From Loss to Output -->
    <line x1="750" y1="170" x2="696" y2="170" class="error-arrow"/>
    <polygon points="750,165 750,175 755,170" fill="#D32F2F"/>

    <!-- From Output to Hidden (thick red arrows) -->
    <line x1="664" y1="170" x2="396" y2="120" class="error-arrow" stroke-width="2.5"/>
    <polygon points="664,165 664,175 669,170" fill="#D32F2F"/>

    <line x1="664" y1="170" x2="396" y2="220" class="error-arrow" stroke-width="2.5"/>

    <!-- From Hidden to Input (curved) -->
    <path d="M 364 120 Q 250 150 96 180" class="error-arrow" stroke-width="2.5"/>
    <path d="M 364 220 Q 250 220 96 260" class="error-arrow" stroke-width="2.5"/>

    <!-- Error labels -->
    <text x="705" y="155" class="grad-label">δ⁽²⁾</text>
    <text x="520" y="135" class="grad-label">δ⁽¹⁾</text>

    <!-- Gradient Computation Nodes (above network) -->
    <rect x="750" y="30" width="100" height="35" rx="4" class="gradient-node"/>
    <text x="800" y="52" text-anchor="middle" fill="#2D6A4F" font-size="13" font-weight="bold">δ⁽²⁾</text>

    <rect x="300" y="30" width="100" height="35" rx="4" class="gradient-node"/>
    <text x="350" y="52" text-anchor="middle" fill="#2D6A4F" font-size="13" font-weight="bold">δ⁽¹⁾</text>

    <!-- Gradient flow arrows (dashed orange) -->
    <path d="M 775 154 Q 800 100 800 65" class="gradient-arrow"/>
    <path d="M 680 150 Q 500 100 350 65" class="gradient-arrow"/>

    <!-- Mathematical Equations -->
    <rect x="50" y="330" width="900" height="45" rx="6" fill="#FFF9E6" stroke="#F57F17" stroke-width="2"/>
    <text x="70" y="350" font-weight="bold" font-size="12" fill="#F57F17">Gradient Computation (Chain Rule):</text>
    <text x="70" y="368" font-size="11" font-family="monospace" fill="#333">δ⁽²⁾ = ∂L/∂a⁽²⁾ ⊙ σ'(z⁽²⁾)     |     δ⁽¹⁾ = (W⁽²⁾)ᵀ δ⁽²⁾ ⊙ σ'(z⁽¹⁾)</text>
</svg>'''
    return svg


# Generate all SVG diagrams
if __name__ == "__main__":
    diagrams = {
        'perceptron_diagram.svg': generate_perceptron_svg(),
        'computational_graph_diagram.svg': generate_computational_graph_svg(),
        'backpropagation_diagram.svg': generate_backpropagation_svg(),
    }

    output_dir = '/Users/njpinton/projects/git/CMSC173/presenter_app/static/diagrams'

    import os
    os.makedirs(output_dir, exist_ok=True)

    for filename, content in diagrams.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"✓ Generated {filepath}")

    print("\nAll SVG diagrams generated successfully!")
