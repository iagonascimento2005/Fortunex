from controllers import FinancialController
from views import FinanceDashboard
import sys

if __name__ == "__main__":
    """Inicializa o sistema de controle financeiro."""
    db_file = "finance.db"
    try:
        controller = FinancialController(db_file)
        app = FinanceDashboard(controller)
        app.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar o aplicativo: {e}")
        sys.exit(1)