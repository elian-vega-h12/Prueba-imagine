# Mutation Baseline

## Status

- Recommendation: blocked

## Commands

- `python -m mutmut run`: failed on native Windows because Mutmut requires WSL.
- `wsl pwd`: passed.
- `wsl bash -lc "... python3 --version"`: failed because `bash` is not executable in the WSL distribution.
- `wsl sh -lc "... python3 --version"`: failed because `python3` is not installed in the WSL distribution.

## Evidence

Mutmut output:

```text
To run mutmut on Windows, please use the WSL.
Native windows support is tracked in issue https://github.com/boxed/mutmut/issues/397
```

## Next Step

Run `mutmut run` in GitHub Actions on Ubuntu or install Python in WSL and run the backend setup there.
