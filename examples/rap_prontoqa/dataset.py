from dataclasses import dataclass, field
from typing import List, Dict, Iterator, Mapping

import json
from dataclasses import dataclass, field
from typing import List, Dict, Iterator, Union


@dataclass
class ProntoQAProblem:
    question: str
    query: str
    chain_of_thought: List[str]
    answer: str





@dataclass
class ProntoQAExample:
    in_context_examples: Mapping[str, ProntoQAProblem]
    test_example: ProntoQAProblem = field(default=None)


@dataclass
class ProntoQADataset:
    examples: Dict[str, ProntoQAExample] = field(default_factory=dict)

    @classmethod
    def from_file(cls, file_path: str) -> 'ProntoQADataset':
        instance = cls()
        with open(file_path, 'r') as f:
            raw_data = json.load(f)

        for example_key, example_value in raw_data.items():

            all_examples = {
                k: ProntoQAProblem(
                    question=e["question"],
                    query=e["query"],
                    chain_of_thought=e["chain_of_thought"],
                    answer=e["answer"]
                ) for k, e in example_value.items()
            }

            test_example = all_examples.pop('test_example', None)
            in_context_examples = all_examples

            instance.examples[example_key] = ProntoQAExample(in_context_examples, test_example)
            # print(f"example_key: {example_key}, in_context_examples: {in_context_examples} test_example: {test_example}")
            # print("="*50)

        return instance

    def __iter__(self) -> Iterator[Union[ProntoQAProblem, ProntoQAExample]]:
        return iter(self.examples.values())


# Sample usage
if __name__ == "__main__":
    pronto_qa_dataset = ProntoQADataset.from_file('/Users/xiyan/Downloads/345hop_random_true.json')

    for example in pronto_qa_dataset:
        print(example)