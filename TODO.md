# Implementation Plan: Separate Public Landing Preview (/landing)

## Steps:

# Implementation Plan: Separate Public Landing Preview (/landing) - COMPLETE ✅

## Steps:

- [x] Step 1: Add @auth_bp.route('/landing') in routes/auth.py ✅
- [x] Step 2: Update templates/base.html nav logo ✅
- [x] Step 3: Update templates/index.html landing-nav links ✅
- [x] Step 4: Changes ready for testing ✅
- [x] Step 5: Task complete ✅

## Changes Made:
- **routes/auth.py**: New `/landing` route renders index.html always (no login redirect), copies teacher data logic.
- **templates/base.html**: Nav logo → auth.landing
- **templates/index.html**: Landing nav logo + Home link → auth.landing
- **TODO.md**: This file for tracking.

## Test:
1. `python app.py`
2. Visit /landing (logged-out: landing page; logged-in: same landing preview)
3. Visit / (logged-in: redirects to dashboard; logged-out: landing)

Public landing preview now available at /landing for all users!
