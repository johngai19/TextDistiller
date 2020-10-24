# 🍞 TextDistiller: Effortless Document Summarization

**TextDistiller** is an advanced, AI-driven tool designed to summarize books chapter by chapter or as a whole, providing concise yet comprehensive overviews. With TextDistiller, you can quickly grasp the core ideas and key takeaways from any book, saving time while maintaining comprehension.

## Key Features

- **Chapter-wise Summarization**: TextDistiller offers detailed summaries for each chapter, allowing you to focus on specific sections of interest.
- **Entire Book Synopsis**: For books without chapter divisions, TextDistiller condenses the entire text into a coherent summary.
- **Powered by NLP**: Utilizing state-of-the-art Natural Language Processing (NLP) techniques, TextDistiller effectively captures and summarizes the most pertinent content.
- **User-Friendly Interface**: TextDistiller features a clean and intuitive interface, making the summarization process accessible and straightforward for all users.

## How TextDistiller Works

TextDistiller leverages the `T5-small` pretrained model from HuggingFace Transformers to generate accurate and readable summaries. The process includes:

1. **Chunking**: The book is divided into chunks, either by chapter or as a single unit.
2. **Tokenization**: These chunks are tokenized using the `T5Tokenizer` for compatibility with the `T5` model.
3. **Summary Generation**: The tokenized text is processed by the `T5ForConditionalGeneration` model to generate summary token IDs.
4. **Decoding**: The summary token IDs are decoded into human-readable text using the `T5Tokenizer`'s `decode()` function.

## Getting Started

1. Clone the repository:
    ```sh
    git clone https://github.com/johngai19/TextDistiller.git
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. To run via CLI:
    ```sh
    python3 bsCLI.py --path <path-to-PDF-file>
    ```
4. To run on a Flask server with frontend and mail:
    1. Update the `sender_address` and `sender_pass` in `mail.py`.
    2. Run `views.py`:
        ```sh
        python3 views.py
        ```

## Contributing

We welcome contributions from the community! If you'd like to contribute to TextDistiller, please feel free to submit a pull request or open an issue. Your feedback and support are greatly appreciated!

## License

TextDistiller is distributed under the [MIT License](https://github.com/johngai19/TextDistiller/blob/master/LICENSE).

---

*Maintained by [John Ngai](https://github.com/johngai19)*
