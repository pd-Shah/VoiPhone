# add the most.voip library root dir to the current python path...
import sys
sys.path.append("../src/")

# import the Voip Library
from most.voip.api import VoipLib

# instanziate the lib
my_voip = VoipLib()
