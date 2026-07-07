import subprocess
import os
import sys

def compile_executive_summary():
    tex_content = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{a4paper, margin=1in}
\usepackage{amsmath}
\usepackage{tcolorbox}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{titlesec}
\usepackage{enumitem}

\definecolor{corporatenavy}{RGB}{0, 32, 96}
\definecolor{corporateblue}{RGB}{0, 112, 192}

\titleformat{\section}{\Large\bfseries\color{corporatenavy}}{}{0em}{}[\titlerule]

\begin{document}

\begin{center}
    {\huge \bfseries \color{corporatenavy} FMCG Market Basket Studio} \\[0.5cm]
    {\Large \color{corporateblue} Executive Summary \& Technical Architecture} \\[0.5cm]
    \rule{\textwidth}{0.4pt}
\end{center}

\vspace{0.5cm}

\section*{Strategic Objective}
To transition traditional market basket analysis from statistical observation to automated margin expansion.
By leveraging Expected Commercial Value (ECV) and FP-Growth algorithms, this engine identifies
high-profit cross-selling opportunities for E-commerce recommendation systems.

\vspace{0.5cm}

\begin{tcolorbox}[colback=corporateblue!5!white,colframe=corporatenavy,title=\textbf{Core Architecture}]
\begin{itemize}[leftmargin=*]
    \item \textbf{Data Ingestion:} DuckDB engine for out-of-core processing of million-row transaction logs.
    \item \textbf{Algorithmic Engine:} FP-Growth for efficiency, eliminating Apriori's bottleneck.
    \item \textbf{API Layer:} FastAPI microservice delivering JSON responses for real-time checkout.
    \item \textbf{UI Layer:} Streamlit dashboard featuring NetworkX affinity graphs for category managers.
\end{itemize}
\end{tcolorbox}

\vspace{0.5cm}

\section*{Commercial Valuation Metric (ECV)}
The core differentiator of this engine is the monetization of statistical confidence.
The Expected Commercial Value is calculated as:
\vspace{0.3cm}
\begin{center}
$ECV = P(\text{Consequent} | \text{Antecedent}) \times Margin_{\text{Consequent}} \times V$
\end{center}
\vspace{0.3cm}
Where $V$ represents the expected baseline volume (e.g., 1,000 baskets).
This allows merchandising teams to prioritize gross margin impact over raw statistical lift.

\vspace{0.5cm}

\section*{Deployment Pipeline}
The repository enforces strict CI/CD standards, utilizing \texttt{uv} for dependency resolution,
\texttt{ruff} for strict linting, and \texttt{pytest} for backend validation.
The architecture supports both local parquet file ingestion and enterprise Google BigQuery integrations.

\end{document}
"""

    tex_filename = "executive_summary.tex"

    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print("Compiling Executive Summary PDF via pdflatex...")

    try:
        subprocess.run(["pdflatex", tex_filename], check=True)
        print("PDF generated successfully.")
    except subprocess.CalledProcessError:
        print("LaTeX compilation failed. See the output above for the specific LaTeX error.", file=sys.stderr)
        sys.exit(1)
    finally:
        for ext in ['.aux', '.log', '.out', '.tex']:
            file_to_remove = tex_filename.replace('.tex', ext)
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)

    if not os.path.exists('assets'):
        os.makedirs('assets')
    if os.path.exists('executive_summary.pdf'):
        os.replace('executive_summary.pdf', 'assets/executive_summary.pdf')

if __name__ == "__main__":
    compile_executive_summary()
