{ pkgs, ... }:

{
  # Enable devenv shell features
  packages = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv = {
      enable = true;
      requirements = ./requirements.txt;
    };
  };

  # Project scripts
  scripts.start.exec = "uvicorn src.main:app --reload --host 0.0.0.0 --port 8000";
  scripts.pytest.exec = "python -m pytest";
  scripts.lint.exec = ''
    black src/ tests/
    flake8 src/ tests/
  '';
  scripts.docker-build.exec = "docker build -t api-wrapper:latest .";
  scripts.docker-run.exec = "docker run --rm -p 8000:8000 api-wrapper:latest";

  # Environment variables
  env = {
    PYTHONPATH = ".:$PYTHONPATH";
  };

  # Pre-commit hooks
  pre-commit.hooks = {
    black.enable = true;
    flake8.enable = true;
  };

  # Enter the environment
  enterShell = ''
    echo "🐍 Python API Wrapper development environment"
    echo "Available commands:"
    echo "  start        - Run the development server"
    echo "  pytest       - Run tests"
    echo "  lint         - Run linters"
    echo "  docker-build - Build the Docker image"
    echo "  docker-run   - Run the Docker container"
  '';
}
