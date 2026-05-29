import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doc_review_agent.config import ConfigError, load_llm_config


class ConfigTests(unittest.TestCase):
    def test_loads_openai_compatible_config_from_environment(self):
        env = {
            "OPENAI_API_KEY": "sk-test",
            "OPENAI_BASE_URL": "https://example.com/v1",
            "OPENAI_MODEL": "custom-model",
        }

        with patch.dict(os.environ, env, clear=True):
            config = load_llm_config()

        self.assertEqual(config.api_key, "sk-test")
        self.assertEqual(config.base_url, "https://example.com/v1")
        self.assertEqual(config.model, "custom-model")

    def test_defaults_to_aihubmix_base_url_and_model(self):
        env = {"OPENAI_API_KEY": "sk-test"}

        config = load_llm_config(env=env, keyring_get_password=lambda service, username: None)

        self.assertEqual(config.api_key, "sk-test")
        self.assertEqual(config.base_url, "https://aihubmix.com/v1")
        self.assertEqual(config.model, "gpt-4o-mini")

    def test_loads_api_key_from_aihubmix_keyring_entry(self):
        calls = []

        def fake_keyring(service, username):
            calls.append((service, username))
            return "sk-keyring"

        with patch.dict(os.environ, {}, clear=True):
            config = load_llm_config(keyring_get_password=fake_keyring)

        self.assertEqual(config.api_key, "sk-keyring")
        self.assertEqual(config.base_url, "https://aihubmix.com/v1")
        self.assertEqual(calls, [("aihubmix", "sjqy")])

    def test_allows_keyring_service_and_username_overrides(self):
        env = {
            "AIHUBMIX_KEYRING_SERVICE": "custom-service",
            "AIHUBMIX_KEYRING_USERNAME": "custom-user",
        }
        calls = []

        def fake_keyring(service, username):
            calls.append((service, username))
            return "sk-custom"

        config = load_llm_config(env=env, keyring_get_password=fake_keyring)

        self.assertEqual(config.api_key, "sk-custom")
        self.assertEqual(calls, [("custom-service", "custom-user")])

    def test_requires_api_key_from_env_or_keyring(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                load_llm_config(keyring_get_password=lambda service, username: None)

        message = str(ctx.exception)
        self.assertIn("OPENAI_API_KEY", message)
        self.assertIn("aihubmix", message)
        self.assertIn("sjqy", message)


if __name__ == "__main__":
    unittest.main()
