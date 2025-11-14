"""Project-wide constant definitions for the Mistral agent."""

from __future__ import annotations

from pathlib import Path

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI service-developer focused on generating new services. "
    "Study the design guide, checklist, and all provided service examples before planning your response. "
    "Consult any provided API specification carefully and include every required parameter when configuring endpoints. "
    "Mirror their structure, naming, and branching conventions. The user’s regular prompt describes the "
    "service to build, and your final answer must be valid JSON that encodes the resulting service definition "
    "while satisfying every checklist rule. "
    "Always detect the language of the current user prompt and respond exclusively in that language, ignoring any prior prompt language. "
    "Never wrap assignment values in backticks or Markdown fences—return plain text or `${var}` placeholders only, regenerating the step if needed."
)

EXAMPLES_DIR = Path(__file__).with_name("examples")

DEFAULT_CONTEXT_FILENAMES: list[str] = []

DEFAULT_CONTEXT_PATHS = [EXAMPLES_DIR / name for name in DEFAULT_CONTEXT_FILENAMES]

SERVICE_DESIGN_GUIDE_PATH = Path(__file__).with_name("SERVICE_DESIGN_GUIDE.md")

try:
    SERVICE_DESIGN_GUIDE = SERVICE_DESIGN_GUIDE_PATH.read_text(encoding="utf-8")
except OSError:
    SERVICE_DESIGN_GUIDE = "Service design guide not found."
SERVICE_CHECKLIST_PATH = Path(__file__).with_name("SERVICE_CHECKLIST.json")

try:
    SERVICE_CHECKLIST = SERVICE_CHECKLIST_PATH.read_text(encoding="utf-8")
except OSError:
    SERVICE_CHECKLIST = "{}"


# NATIONAL HOLIDAYS
# National holidays ALL - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that returns current national holidays of the current year, for Estonia. Use this API-t: https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis kõik käesoleva aasta Eesti riigipühad. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# National holidays YTD - OK
#DEFAULT_SAMPLE_QUESTION = "Build a service that retrieves Estonia’s national holidays for the current year - year-to-date — from January 1st up to today — using the OpenHolidays API (spec: https://openholidaysapi.org/swagger/v1/swagger.json)."
DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis tagastab käesoleva aasta Eesti riigipühad aasta algusest kuni tänase kuupäevani. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# National holidays EOY - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that returns the national holidays of Estonia from current day to the end of the year. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis tagastab Eesti riigipühad käesoleva aasta tänasest päevast aasta lõpuni. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# National holidays NEXT - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that returns the next upcoming national holiday in Estonia. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis tagastab järgmise Eesti riigipüha. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# National holidays PREVIOUS - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that returns the previous national holiday in Estonia. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis tagastab eelmise Eesti riigipüha. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# National holidays TODAY - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that returns whether today is a national holiday in Estonia. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis tagastab, kas täna on Eesti riigipüha. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json" 

# National holidays SEARCH - OK
#DEFAULT_SAMPLE_QUESTION = "Create a service that takes national holiday name in Estonia as input an returns at what time is the holiday in the current year. Use this api : https://openholidaysapi.org/swagger/v1/swagger.json"
#DEFAULT_SAMPLE_QUESTION = "Loo teenus, mis võtab sisendiks Eesti riigipüha nime ja tagastab, mis ajal on antud püha käesoleval aastal. Kasuta seda API-t: https://openholidaysapi.org/swagger/v1/swagger.json"

# Currency exchange rate - OK
#DEFAULT_SAMPLE_QUESTION = "Loo mulle valuuta võrdluse teenuse. Teenuse sisendiks on valuuta kood, mille edastab kasutaja. Ning tagasta antud valuuta kurss vastu Eurot"

#DEFAULT_SAMPLE_QUESTION = "Loo mulle valuuta võrdluse teenuse. Teenuse sisendiks on valuuta kood, mille edastab kasutaja. kui antud valuuta koodi pole või ta on olematu tagasta teavitus, et antud valuutakoodi ei leitud. Teenuse sisendi peab muutma suurteks tähtedeks. Kui valuuta kood leitakse, tagasta antud valuuta kurss vastu Eurot"

#DEFAULT_SAMPLE_QUESTION = "Tee teenus, mis tagastab kõige odavama elektrihinna (senti/kWh) Eestis, kogu tänase päeva jooksul. Kasuta seda API https://dashboard.elering.ee/api/nps/price"


DEFAULT_OUTPUT_PATH = Path(__file__).resolve().parent.parent / "service_response.json"
