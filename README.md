# m3u8_merge_tool
Python m3u8 block files merge tool

## Processing step
1. Read m3u8 files context by rows.
2. Every 10 files link to 1 merge files list.
3. Transfer every merge files list to multithread reactor.
4. Every threads processing one shell command to execute "FFMPEG" make 10 ts files to 1 bigger ts file.
5. Continue process there bigger ts files output to final mp4 file.
6. Purge all temp ts files.
7. Files processing and creating at current path.

## Command line for execute
[^file replace]
  ```Bash
  $ m3u8_merge.py <m3u8 file name>
  ```

### Wait a minute, while the command execute finished.

#### PS: This script do not support which m3u8 file with AES key, it supported at [Rust_m3u8_dl](https://github.com/ItiharaYuuko/Rust_m3u8_dl).

Enjoy.

---
[^file replace] Replace the <m3u8 file name> to your file path
