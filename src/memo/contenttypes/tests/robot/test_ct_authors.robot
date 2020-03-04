# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s memo.contenttypes -t test_authors.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src memo.contenttypes.testing.MEMO_CONTENTTYPES_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/memo/contenttypes/tests/robot/test_authors.robot
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

Scenario: As a site administrator I can add a authors
  Given a logged-in site administrator
    and an add authors form
   When I type 'My authors' into the title field
    and I submit the form
   Then a authors with the title 'My authors' has been created

Scenario: As a site administrator I can view a authors
  Given a logged-in site administrator
    and a authors 'My authors'
   When I go to the authors view
   Then I can see the authors title 'My authors'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add authors form
  Go To  ${PLONE_URL}/++add++authors

a authors 'My authors'
  Create content  type=authors  id=my-authors  title=My authors

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the authors view
  Go To  ${PLONE_URL}/my-authors
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a authors with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the authors title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
