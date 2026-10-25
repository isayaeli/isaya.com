import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.test import override_settings

from contact.forms import ContactForm


class Command(BaseCommand):
    help = "Render the portfolio as a static site for GitHub Pages, with the contact form posting to Formspree."

    def add_arguments(self, parser):
        parser.add_argument("--base-url", default=os.getenv("PAGES_BASE_URL", ""), help="Public URL the site is served from.")
        parser.add_argument("--formspree", default=os.getenv("FORMSPREE_ENDPOINT", ""), help="Formspree form endpoint.")
        parser.add_argument("--out", default=str(settings.BASE_DIR / "dist"), help="Output directory.")

    def handle(self, *args, **options):
        base_url = options["base_url"].rstrip("/")
        formspree = options["formspree"]
        if not base_url:
            raise CommandError("Set --base-url or PAGES_BASE_URL.")
        if not formspree:
            raise CommandError("Set --formspree or FORMSPREE_ENDPOINT.")

        out = settings.BASE_DIR / options["out"]
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(settings.BASE_DIR / "static", out / "static")

        with override_settings(STATIC_URL=f"{base_url}/static/"):
            html = render_to_string(
                "index.html",
                {"form": ContactForm(), "static_build": True, "formspree_endpoint": formspree},
            )
        (out / "index.html").write_text(html, encoding="utf-8")
        (out / ".nojekyll").touch()

        self.stdout.write(self.style.SUCCESS(f"Built static site in {out}"))
