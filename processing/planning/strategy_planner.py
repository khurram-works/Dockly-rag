from domain.models.document_profile import DocumentProfile
from domain.models.document_strategy import DocumentStrategy

from processing.planning.strategy_config import STRATEGY_CONFIG

from core.exceptions import UnsupportedDocumentError

class StrategyPlanner:

  def plan(
    self,
    profile: DocumentProfile,
   ) -> DocumentStrategy:

    strategy = STRATEGY_CONFIG.get(profile.extension)
    if strategy is None:
      raise UnsupportedDocumentError(
        f"Unsupported document type: {profile.extension}"
      )

    return strategy



