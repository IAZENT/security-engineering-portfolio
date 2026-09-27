# Security Engineering Portfolio

This repository contains a practical cybersecurity portfolio covering authorized security testing, technical walkthroughs, security research and engineering projects.

## Documentation site

The published documentation site is generated from the `docs/` directory with MkDocs Material.

- Website: [Security Documentation](https://iazent.github.io/security-engineering-portfolio/)
- Source: [GitHub repository](https://github.com/IAZENT/security-engineering-portfolio)

## What this portfolio demonstrates

- Penetration-testing methodology and evidence handling
- Web, infrastructure and application-security testing
- Security research and technical analysis
- Reproducible lab walkthroughs
- Threat modelling and security design decisions
- Remediation guidance and retesting
- Version-controlled technical writing

## Documentation workflow

1. Work only on systems and labs that are owned or explicitly authorized.
2. Keep raw evidence and sensitive material outside the repository.
3. Write the technical report in Dradis or private working notes.
4. Sanitize the public version by removing secrets, personal data and private infrastructure details.
5. Publish the sanitized Markdown document under `docs/`.
6. Run the local lint and build checks.
7. Commit a focused change with a useful message.
8. Push to `main`; GitHub Actions validates and publishes the site.

## Local commands

```bash
./scripts/preview.sh
npm run lint:md
.venv/bin/mkdocs build --strict
```

## Responsible disclosure

All testing documented here is performed in authorized environments, intentionally vulnerable labs or systems for which permission has been granted. Sensitive evidence is deliberately excluded from this public repository.
