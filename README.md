# license-updater

The script was created using [cursor](https://cursor.com/)

## A sample run
```
$ python license_updater.py sample.csv 
Processing package: boost-atomic.x86_64...
/home/lmohanty/Downloads/license-updater/license_updater.py:180: FutureWarning: Setting an item of incompatible dtype is deprecated and will raise an error in a future version of pandas. Value 'BSL-1.0 AND MIT AND Python-2.0.1' has dtype incompatible with float64, please explicitly cast to a compatible dtype first.
  df.loc[index, 'License'] = new_license
  Updated license for boost-atomic.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-chrono.x86_64...
  Updated license for boost-chrono.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-container.x86_64...
  Updated license for boost-container.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-context.x86_64...
  Updated license for boost-context.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-contract.x86_64...
  Updated license for boost-contract.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-coroutine.x86_64...
  Updated license for boost-coroutine.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-date-time.x86_64...
  Updated license for boost-date-time.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-fiber.x86_64...
  Updated license for boost-fiber.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-filesystem.x86_64...
  Updated license for boost-filesystem.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-graph.x86_64...
  Updated license for boost-graph.x86_64: BSL-1.0 AND MIT AND Python-2.0.1
Processing package: boost-iostreams.x86_64...
  Updated license for boost-iostreams.x86_64: BSL-1.0 AND MIT AND Python-2.0.1

--- Updated DataFrame (first 20 rows) ---
| UBI?   | package                 | License                          |
|:-------|:------------------------|:---------------------------------|
| no     | boost-atomic.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-chrono.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-container.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-context.x86_64    | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-contract.x86_64   | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-coroutine.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-date-time.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-fiber.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-filesystem.x86_64 | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-graph.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-iostreams.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |

--- Updated DataFrame (last 20 rows) ---
| UBI?   | package                 | License                          |
|:-------|:------------------------|:---------------------------------|
| no     | boost-atomic.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-chrono.x86_64     | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-container.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-context.x86_64    | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-contract.x86_64   | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-coroutine.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-date-time.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-fiber.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-filesystem.x86_64 | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-graph.x86_64      | BSL-1.0 AND MIT AND Python-2.0.1 |
| no     | boost-iostreams.x86_64  | BSL-1.0 AND MIT AND Python-2.0.1 |
```
