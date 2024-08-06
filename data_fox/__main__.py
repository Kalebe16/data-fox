import sys
from pathlib import Path


def before_run_app() -> None:
    def adjust_python_path() -> None:
        """
        Prepares the environment for running the app with `textual run --dev`
        """
        MODULE_PARENT_PATH = Path(__file__).parent.parent
        if str(MODULE_PARENT_PATH) not in sys.path:
            sys.path.append(str(MODULE_PARENT_PATH))

    adjust_python_path()


def run_app() -> None:
    from data_fox.app import DataFoxApp

    DataFoxApp().run()

def main() -> None:
    before_run_app()
    run_app()

if __name__ == '__main__':
    main()
