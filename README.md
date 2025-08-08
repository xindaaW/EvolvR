# EvolvR: Self-Evolving Pairwise Reasoning for Story Evaluation to Enhance Generation
The full source code will be made publicly available upon acceptance.


```
EvolvR/
├── Baseline/           # Baseline methods
│   ├── CloseLLM/      # Closed-source LLM evaluation
│   └── NLG/           # Open-source NLG model evaluation
├── Evaluation/         # Evaluation modules
│   ├── CoTAgent/      # Chain-of-Thought agent evaluation
│   ├── CoTSynthesis/  # Chain-of-Thought synthesis evaluation
│   ├── GRPO/          # GRPO-based evaluation model training
│   ├── InferTest/     # Inference testing
│   └── Pointwise/     # Pointwise evaluation
└── Generation/         # Generation modules
    ├── GRPO/          # GRPO-based story generation
    └── SFT/           # Supervised fine-tuning story generation
```

## 🚀 Core Features

### 1. Multi-dimensional Story Evaluation

The project supports comprehensive story evaluation from six dimensions:

- **Relevance**: Degree of match between content and themes/requirements
- **Coherence**: Fluency and consistency of content logic and structure
- **Empathy**: Understanding and resonance with others' emotions and situations
- **Surprise**: Unexpected and novel feelings brought by content
- **Engagement**: Degree of audience involvement and interaction
- **Complexity**: Complexity of content in terms of structure and connotation

### 2. Chain-of-Thought Evolutionary Evaluation

#### CoTAgent Module
Integrates four Chain-of-Thought screening and evolution methods:
- **CoT_RuleCheck.py**: Rule-based Chain-of-Thought checking
- **CoT_Logit.py**: Logic-based Chain-of-Thought analysis
- **CoT_SelfCheck.py**: Self-checking Chain-of-Thought verification
- **CoT_Robust.py**: Robust Chain-of-Thought evaluation

#### CoTSynthesis Module
Provides multiple Chain-of-Thought synthesis methods:
- **infer_multi_persona.py**: Multi-persona Chain-of-Thought synthesis
- **infer_pair.py**: Pairwise comparison Chain-of-Thought synthesis

### 3. Reinforcement Learning Optimization

#### GRPO (Group Relative Policy Optimization)
- **Data Preprocessing**: Prompt-based segmentation and reward function design
- **Evaluation Model Training**: Training evaluation models using reinforcement learning
- **Story Generation Optimization**: Optimizing generation quality through reward signals

## 📁 Detailed Module Description

### Baseline Module

#### CloseLLM/
- **CloseLLM.py**: Closed-source large language model evaluation implementation
- **CloseLLM_StoryER.py**: Closed-source model testing for story evaluation

#### NLG/
- **TigerScore.py**: TigerScore evaluation method
- **Themis.py**: Themis evaluation framework
- **AutoJ.py**: AutoJ automatic evaluation tool
- **OpenMEVA Version**: Evaluation adaptation for OpenMEVA dataset

### Evaluation Module

#### CoTAgent/
- **CoT_RuleCheck.py**: Rule-based Chain-of-Thought checking
- **CoT_Logit.py**: Logic-based Chain-of-Thought analysis
- **CoT_SelfCheck.py**: Self-checking Chain-of-Thought verification
- **CoT_Robust.py**: Robust Chain-of-Thought evaluation

#### CoTSynthesis/
- **Multi-persona Evaluation**: Story evaluation from different persona perspectives
- **Pairwise Comparison**: Enhancing evaluation accuracy through comparative analysis
- **Chain-of-Thought Synthesis**: Integrating thinking processes from multiple evaluation perspectives

#### GRPO/
- **StoryER_data_process.py**: StoryER dataset preprocessing
- **HANNA_data_process.py**: HANNA dataset preprocessing
- **Reward Calculation**: Multi-dimensional evaluation-based reward function design

#### InferTest/
- **infer_test.py**: Basic inference testing
- **infer_test_OpenMEVA.py**: OpenMEVA dataset inference testing
- **infer_test_pair_sameinput.py**: Same input pairwise inference testing
- **infer_test_pair_diffinput.py**: Different input pairwise inference testing

#### Pointwise/
- **infer_point.py**: Pointwise evaluation implementation, supporting detailed content analysis and scoring process

### Generation Module

#### GRPO/
- **prompt_Divide.py**: Prompt segmentation strategy
- **data_preprocess.py**: Data preprocessing pipeline
- **infer_Qwen2.5_7B.py**: Inference implementation based on Qwen2.5-7B

#### SFT/
- **above3.py**: Supervised fine-tuning training based on high-score data
