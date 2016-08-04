"""
class AQ_EXPORT FLTranslations
{

public:

  typedef QPtrList<MetaTranslatorMessage> TML;

  bool loadTsFile(MetaTranslator &tor, const QString &tsFileName, bool /* verbose */);

  void releaseMetaTranslator(const MetaTranslator &tor,
                             const QString &qmFileName, bool verbose,
                             bool stripped);

  void releaseTsFile(const QString &tsFileName, bool verbose,
                     bool stripped);

  void lrelease(const QString &tsInputFile, const QString &qmOutputFile, bool stripped = true);
};
"""