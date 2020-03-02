# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_manuscript.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_manuscript.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a manuscript
  Given a logged-in site administrator
    and an add manuscript form
   When I type 'My manuscript' into the title field
    and I submit the form
   Then a manuscript with the title 'My manuscript' has been created

Scenario: As a site administrator I can view a manuscript
  Given a logged-in site administrator
    and a manuscript 'My manuscript'
   When I go to the manuscript view
   Then I can see the manuscript title 'My manuscript'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add manuscript form
  Go To  ${PLONE_URL}/++add++manuscript

a manuscript 'My manuscript'
  Create content  type=manuscript  id=my-manuscript  title=My manuscript

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the manuscript view
  Go To  ${PLONE_URL}/my-manuscript
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a manuscript with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the manuscript title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
