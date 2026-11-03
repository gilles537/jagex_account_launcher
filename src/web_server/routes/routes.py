from account_launcher.account_launcher import AccountLauncher, JagexAccount
from flask import jsonify, render_template, request
from loguru import logger
from web_server.services.account_manager import AccountManager


def setup_routes(app, account_manager: AccountManager, account_launcher: AccountLauncher):
    @app.route("/")
    def index():
        return render_template(
            "index.html",
            accounts=account_manager.get_accounts(),
            notification={},
        )

    @app.route("/get_accounts", methods=["GET"])
    def get_accounts():
        return jsonify(account_manager.get_accounts())

    @app.route("/add_account", methods=["POST"])
    def add_account():
        try:
            account_data = request.json
            new_nickname = account_data.pop("nickname")
            logger.info(f"Adding account with data: {account_data}")
            account_manager.add_account(new_nickname, account_data)
            return jsonify({"status": "success", "message": "Account added successfully."}), 201
        except Exception as e:
            logger.exception("Failed to add account.")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/update_account", methods=["PUT"])
    def update_account():
        try:
            account_data = request.json
            original_nickname = account_data.pop("originalNickname")
            new_nickname = account_data.pop("nickname")
            logger.info(f"Updating account {original_nickname} with data: {account_data}")
            account_manager.update_account(original_nickname, new_nickname, account_data)
            return jsonify({"status": "success", "message": "Account updated successfully."}), 200
        except Exception as e:
            logger.exception("Failed to update account.")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/delete_account", methods=["POST"])
    def delete_account():
        try:
            nickname = request.json["nickname"]
            logger.info(f"Deleting account {nickname}")
            account_manager.delete_account(nickname)
            return jsonify({"status": "success", "message": "Account deleted successfully."}), 200
        except Exception as e:
            logger.exception("Failed to delete account.")
            return jsonify({"status": "error", "message": f"Internal Server Error: {e}"}), 500

    @app.route("/launch_account", methods=["POST"])
    def launch_account():
        account_id = request.json["account_id"]
        logger.info(f"Launching account: {account_id}")

        try:
            account_data = account_manager.get_accounts()[account_id]
            jagex_account = JagexAccount(
                JX_CHARACTER_ID=account_data["JX_CHARACTER_ID"],
                JX_SESSION_ID=account_data["JX_SESSION_ID"],
                JX_DISPLAY_NAME=account_data["JX_DISPLAY_NAME"],
                JX_REFRESH_TOKEN=account_data.get("JX_REFRESH_TOKEN", ""),
                JX_ACCESS_TOKEN=account_data.get("JX_ACCESS_TOKEN", ""),
            )
            account_launcher.launch_account(jagex_account)
            return jsonify({"status": "success", "message": "Account launched"}), 200
        except Exception as e:
            logger.exception("Failed to launch account.")
            return jsonify({"status": "error", "message": str(e)}), 500
