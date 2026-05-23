# Distributed Computing - Banking App

# Getting started for *nix

Requirements: ensure that you have `python`/`python3` installed and working (test with `python --version`)

```sh
python3 -m venv .venv/

source .venv/bin/activate

deactivate

pip install -r requirements.txt

./regenerate_protobufs.sh

python main.py
```

# Getting started for Windows

Get Python from https://www.python.org/downloads/. Install, and when completed, verify install from PowerShell with:

```powershell
python --version
# Python 3.14.5
```

If you want to isolate a python environment specifically for this application (recommended, but you are on your own if you diverge and do things yourself), run the following commands on the repository root:

```powershell
# Create environment  (only do once)
python3 -m venv banking-env

# Activate with
.\banking-env\Scripts\Activate.ps1

# If having issues running the script above, run the following script, but may require elevation (UAC):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Install the dependencies of this application by running:
```powershell
pip install -r requirements.txt
```

When you receive this codebase from elsewhere but GitHub, you are likely already provided with the gRPC protobuf compiled files, located in `grpc_generated/`. Regardless if you have the files or not, it is recommended that you regenerate them with:

```powershell
./regenerate_protobufs.ps1

# Alternatively:
python -m grpc_tools.protoc -I grpc_generated=protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/BankingApp.proto

python -m grpc_tools.protoc -I grpc_generated=protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/InternalBanking.proto
```

# Running the migrations

The application needs a starting dataset to be able to do anything with it. Run the migration by running the [`main.py`](./main.py) and select the **migration** option

```powershell
python main.py
Run:

[1] BDB
[2] BAS
[3] BC
[4] BDB Migrations
[5] BDB Worker (Advanced)
[any other key] to exit

Choice:
```

Select option 4 and it should complete it with:

```powershell
Choice: 4
Done.
```

# Running the application

There are three applications that need to run in tandem here, requiring three different shells running at the same time with the `banking-env` virtual environment running.

Running [`main.py`](./main.py) will give you the option to run either BDB, BAS and BC. It is recommended that you BDB > BAS > BC in sequence on separate shells.

## Troubleshooting

### _ERROR_MESSAGE_PORT_BINDING_FAILED (Failed to bind to address)

This error has been observed on the UAT process of the application when run on Windows. This has not been observed on other platforms such as *nix.

A fix has been made to make this run on Windows. But if this issue still still prevalent for some users, it can be simply mitigated by changing the ports used by the application. Currently, the ports used are and are defined in:
- `10051` - Used by [BAS (Backend.ports)](./bas/Backend.py)
- `10061` - Used by [BDB (Backend.ports)](./bas/Backend.py)
