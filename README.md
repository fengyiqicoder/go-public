# go-public

An Agent skill: turn a workflow you just ran with your AI into a web page anyone can open and use. No account and no API key for visitors.

```bash
npx skills add fengyiqicoder/go-public
```

Other ways to install:

- Claude Code plugin: `/plugin marketplace add fengyiqicoder/go-public`, then `/plugin install go-public@go-public`
- Gemini CLI: `gemini extensions install https://github.com/fengyiqicoder/go-public`
- Any agent that reads skills: copy `skills/go-public/` into its skills folder

Then, after you get something working in Claude Code, Codex or another agent, say "go public". The agent writes the workflow down (inputs, AI steps, outputs) and tests it on a real example. It then builds a single-file page and publishes it, and you get a link.

- **Visitors**: open the link, fill in the input, press Run. No sign-up.
- **You**: nothing to host and no key to protect. To change the page, edit and publish again from the same folder; the link stays the same.
- **Limits**: each page has a free daily AI allowance and a per-visitor rate limit. Pages run in a sandbox: no outside requests except the AI call, and no forms that post anywhere.

## Example

`tests/example-workflow.json` is a two-step workflow (meeting notes → decisions → follow-up email). Try it:

```bash
python3 skills/go-public/share.py try tests/example-workflow.json
```

## Privacy

The published page and the text visitors type go to OneTag AI to run the AI steps; prompts, inputs and answers are not stored. See https://onetagai.com/privacy.

AI calls run on [OneTag AI](https://onetagai.com). Licence: MIT.
