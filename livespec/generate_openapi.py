import importlib
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m livespec.generate_openapi <app_module> <output_file>")
        sys.exit(1)

    app_module = sys.argv[1]
    output_file = Path(sys.argv[2])

    try:
        module = importlib.import_module(app_module)
    except ImportError as e:
        print(f"Cannot import module {app_module}: {e}")
        sys.exit(1)

    app = getattr(module, "app", None)
    if app is None:
        print("Module must expose Flask 'app' variable")
        sys.exit(1)

    spec_dict = app.apispec.to_dict()
    output_file.write_text(app.json.dumps(spec_dict, indent=2))
    print(f"OpenAPI spec written to {output_file}")


if __name__ == "__main__":
    main()
