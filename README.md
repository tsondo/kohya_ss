# kohya_ss (Tsondo fork)

This is a personal fork of [kohya_ss](https://github.com/bmaltais/kohya_ss).  
The upstream project is under active development and continues to add features and improvements. This fork is not intended to replace or compete with upstream — it exists to provide:

- A **stable, reproducible environment** for training and experimentation.
- Documentation of the process for building **xFormers** from source in a way that others can repeat.
- A place to explore fixes and adjustments (for example, investigating issues like the LoRA tab behavior) without disrupting upstream’s fast pace.

---

## Requirements

- Upstream maintains its own `requirements.txt`, which reflects the project’s evolving baseline.
- This fork adds a pinned lockfile: **`requirements.tsondo`**  
  Use this file if you want a guaranteed working environment:

  ```bash
  pip install -r requirements.tsondo
  ```

- For details on building xFormers, see [BUILD_XFORMERS.md](BUILD_XFORMERS.md).

---

## Syncing with Upstream

This fork tracks upstream’s `master` branch. To pull in updates:

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

---

## Notes

- If you want the latest features and updates, use upstream.  
- If you want a **stable, reproducible training stack**, this fork may be useful.  
- Full credit goes to the upstream maintainers for their ongoing work — this fork simply adds a reproducibility layer on top.
