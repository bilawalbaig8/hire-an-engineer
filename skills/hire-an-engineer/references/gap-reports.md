# Gap reports

Read when the person agrees to report a gap in this skill.

1. **Offer once**, at a natural pause, in their language. Never mid-task, never twice.
2. **Draft a short, anonymised report:** area, tool, what happened, what was expected, suggested fix. No project names, code, error output, paths, URLs, service names, data, keys or personal details.
3. **Tell them** it will be public and will show their GitHub name. Show the exact text.
4. **Default route:** a pre-filled link they review and submit themselves:
   `https://github.com/bilawalbaig8/hire-an-engineer/issues/new?template=gap_report.yml&title=[gap]+…`
5. **CLI route** only if they prefer it and approve the exact text:
   `gh issue create --repo bilawalbaig8/hire-an-engineer --title "[gap] …" --body "…"`
   No `--label`; labels come from the template.
6. **Never submit without their explicit OK.**
