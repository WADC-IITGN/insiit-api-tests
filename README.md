##### Please note that you will need to fork this repository and then clone your own version of it on your computer, otherwise you will not be able to contribute.

### Installing dependencies on a new machine

Fork and clone the repository on your computer.

Open a terminal in the root of the repository and run the command:

```bash
pip install -r requirements.txt
```

Then, create a new `.env` file in the root of the repository, and add the following variables to it:

```env
PORT=your_docker_container_port
API_KEY=your_api_key
```

### Running the tests

Open a terminal in the root of the repository.

To run all the tests, run the following command:

```bash
pytest
```

To run tests only from a specific file, run the above command followed by the file name. For example:

```bash
pytest test_root.py
```

### Contributing to the repository

Whenever you commit any new changes, make sure to push them to your forked version of the repository. Then, create a new pull request and provide a meaningful summary and description. After review, your commit will be merged to this repository.
