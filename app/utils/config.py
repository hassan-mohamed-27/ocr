"""
Configuration constants for the application.

Constants:
    CREDENTIALS_PATH (str): Path to Google OAuth2 credentials file
    TOKEN_PATH (str): Path to store OAuth2 tokens
    DOWNLOADS_DIR (str): Directory for downloaded and processed files

Note:
    All paths are relative to the application root directory
    Ensure write permissions for TOKEN_PATH and DOWNLOADS_DIR
"""

CREDENTIALS_PATH = 'client_secret.json'
TOKEN_PATH = 'token.json'
DOWNLOADS_DIR = 'downloads'