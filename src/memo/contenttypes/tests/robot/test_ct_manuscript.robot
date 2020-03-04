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

Scenario: As a site administrator I can add a Manuscript
  Given a logged-in site administrator
    and an add Manuscript form
   When I type 'My Manuscript' into the title field
    and I submit the form
   Then a Manuscript with the title 'My Manuscript' has been created

Scenario: As a site administrator I can view a Manuscript
  Given a logged-in site administrator
    and a Manuscript 'My Manuscript'
   When I go to the Manuscript view
   Then I can see the Manuscript title 'My Manuscript'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Manuscript form
  Go To  ${PLONE_URL}/++add++Manuscript

a Manuscript 'My Manuscript'
  Create content  type=Manuscript  id=my-manuscript  title=My Manuscript

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Manuscript view
  Go To  ${PLONE_URL}/my-manuscript
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Manuscript with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Manuscript title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
