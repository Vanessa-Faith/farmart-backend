# Team Lead Guide - Vanessa

**Your Role:** Project manager, code reviewer, blocker remover, team motivator

This guide covers everything you need to lead the team successfully through the 2-week sprint.

---

## 📊 Overview Dashboard

**Team Size:** 5 people (including you)
**Timeline:** 2 weeks (Jan 29 - Feb 11, 2026)
**Your Feature:** Authentication (backend + frontend)

**Team Assignments:**
- ✅ **Vanessa** - Authentication (YOU - in testing)
- 🔨 **Tecla** - Animals Listings
- 🔨 **Raniel** - Shopping Cart  
- 🔨 **Jonah** - Orders & Payment
- 🔨 **Linda** - QA & Testing

---

## 🎯 Your Daily Responsibilities

### Morning (15-30 minutes)
1. **Check GitHub**
   - Any new PRs? → Review within 24 hours
   - Any issues/questions? → Respond ASAP
   - Any blocked team members? → Unblock them

2. **Run Daily Standup** (15 minutes sharp)
   - Ask each person: What done? What today? Any blockers?
   - Take notes on blockers
   - Don't let it run over - detailed discussions happen after

3. **Update Project Board** (if using GitHub Projects)
   - Move cards: To Do → In Progress → Done
   - Check if anyone is stuck on same task for 2+ days

### Throughout Day (as needed)
- **Respond to team questions** (aim for <2 hour response time)
- **Review PRs** (see detailed guide below)
- **Pair program** if someone is stuck (30 min max, then escalate)
- **Test integrated features** after merges

### Evening (10 minutes)
- **Check team progress** - is anyone falling behind?
- **Plan tomorrow** - what needs priority?
- **Update yourself** - commit your own work!

---

## 🔍 Reviewing Pull Requests (MOST IMPORTANT)

### When PR Comes In

**Goal: Review within 24 hours (ideally same day)**

#### Step 1: Read the PR Description
- Does it explain what was built?
- Does it list what was tested?
- Is there a checklist of completed items?

If description is lacking → **Request changes**: "Please add testing details"

#### Step 2: Check the Code (GitHub)
1. Click "Files changed" tab
2. Look for:
   - ✅ Code follows patterns (like your auth feature)
   - ✅ No hardcoded secrets (API keys, passwords)
   - ✅ Variable names make sense
   - ✅ No commented-out code left behind
   - ✅ No `console.log()` spam or debug prints
   - ⚠️ Red flags: Huge functions (>50 lines), duplicated code, no error handling

**Leave comments:** Click line number → Add comment
- "Great use of error handling here! 👍"
- "Could we extract this into a separate function?"
- "This will cause an error if user is null - add a check?"

#### Step 3: Test It Locally (CRITICAL)

**Backend PR:**
```bash
cd ~/Development/code/se-prep/phase-5/farmart-backend

# Get their branch
git fetch origin
git checkout feature/their-feature-name

# Start backend
source .venv/bin/activate
python run.py

# Test their endpoints
curl http://localhost:5000/api/animals
curl -X POST http://localhost:5000/api/animals \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Cow","species":"cattle","price":500}'
```

**Frontend PR:**
```bash
cd ~/Development/code/se-prep/phase-5/farmart-frontend

# Get their branch
git fetch origin
git checkout feature/their-feature-name

# Install any new dependencies
npm install

# Start frontend
npm run dev

# Test in browser
# - Click all buttons
# - Fill all forms
# - Try invalid inputs
# - Check console for errors (F12)
```

**Integration Test (Backend + Frontend together):**
```bash
# Terminal 1: Run backend
cd farmart-backend && source .venv/bin/activate && python run.py

# Terminal 2: Run frontend
cd farmart-frontend && npm run dev

# Browser: Test the full flow
# Example for Animals: Browse → Search → View Detail → Add to Cart
```

#### Step 4: Make a Decision

**Option 1: Approve ✅**
```markdown
Tested locally and everything works great! 🎉

**What I tested:**
- ✅ All endpoints respond correctly
- ✅ UI looks good and functions properly
- ✅ No errors in console
- ✅ Integrates well with existing features

**Code review:**
- ✅ Follows our patterns
- ✅ Good error handling
- ✅ Clean, readable code

Approving! Ready to merge.
```

**Option 2: Request Changes 🔴**
```markdown
Great progress! Found a few issues that need fixing:

**Bugs:**
- [ ] The delete endpoint returns 500 error - add null check on line 45
- [ ] Cart total shows NaN when empty - handle empty state

**Code quality:**
- [ ] Please remove console.logs on lines 23, 45, 67
- [ ] Extract the calculation logic into a separate function (lines 100-150 too long)

**Testing:**
- [ ] Please test with empty cart scenario
- [ ] Test with invalid animal ID

Let me know when these are fixed and I'll re-review! 👍
```

**Option 3: Comment Only 💬**
```markdown
Looks good overall! A few suggestions (not blocking):

**Nice to have:**
- Could add loading spinner while fetching
- Might want to add pagination if animal list gets long

**Questions:**
- Is the 10 second timeout intentional on line 34?

Not blocking merge, just curious about your approach!
```

#### Step 5: Merge (if Approved)

**Wait for at least 2 approvals:**
- Your approval
- One other team member approval

**Then merge:**
1. On GitHub PR page, click **"Merge pull request"**
2. Choose **"Squash and merge"** (combines all commits into one clean commit)
3. Edit commit message if needed: `Feature: Animals Listings (Tecla) (#PR_NUMBER)`
4. Click **"Confirm squash and merge"**
5. Click **"Delete branch"** (keeps repo clean)

**After merging:**
```bash
# Update YOUR local dev branch
git checkout dev
git pull origin dev

# Tell team in chat
"✅ Merged Animals feature to dev! Everyone pull latest dev before continuing."
```

---

## 🚨 Handling Common Team Issues

### Issue: "I'm stuck and don't know what to do"

**Your response:**
1. **Ask clarifying questions:**
   - "What have you tried so far?"
   - "What error are you seeing?"
   - "Can you show me your code?"

2. **Guide, don't solve:**
   - ❌ "Here's the code, copy this"
   - ✅ "Check how the auth feature does it"
   - ✅ "Try console.log to see what data you're getting"
   - ✅ "Google this error - it's common"

3. **Pair program if needed:**
   - Screen share for 30 minutes
   - Walk through problem together
   - Let THEM type and figure it out

4. **Know when to escalate:**
   - If stuck for >2 hours → bring in another team member
   - If it's blocking others → highest priority

### Issue: "Their PR has been open for 3 days"

**Your response:**
1. **Check why:**
   - Did you request changes? → Follow up: "Any update on the fixes?"
   - Waiting for another reviewer? → Ping them: "Can you review this today?"
   - Forgot about it? → Review it NOW

2. **Set expectation:**
   - "Our goal is 24 hour review time - let's keep things moving!"

### Issue: "Two features conflict - merge conflict"

**Your response:**
1. **Don't panic** - this is normal
2. **Identify which features:**
   - Did both people edit the same file?
   - Did both change the same lines?

3. **Resolve together:**

**What's happening:** Two people edited the same lines of code differently. Git doesn't know which version to keep, so it asks you to decide.

**Example scenario:** 
- Tecla added a new animal field on her branch
- Meanwhile, Raniel merged his changes to dev that modified the same file
- When Tecla tries to merge dev into her branch, CONFLICT!

```bash
# The person whose PR is still open does this
git checkout feature/animals  # Tecla's branch
git merge dev  # Git says: "CONFLICT in app/models/animal.py"
```

**Git marks the conflict in the file like this:**

```python
# app/models/animal.py looks like this after conflict:

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
<<<<<<< HEAD
    species = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    age = db.Column(db.Integer)  # Tecla added this
=======
    species = db.Column(db.String(50), nullable=False) 
    weight = db.Column(db.Float)  # Raniel added this from dev
>>>>>>> dev
    price = db.Column(db.Float, nullable=False)
```

**What the markers mean:**
- `<<<<<<< HEAD` = Start of YOUR code (Tecla's version on her branch)
- `=======` = Divider between the two versions
- `>>>>>>> dev` = End of THEIR code (what's in dev branch)

**How to fix:**

**Option 1: Keep BOTH changes** (usually the right choice)
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    age = db.Column(db.Integer)  # Keep Tecla's addition
    weight = db.Column(db.Float)  # Keep Raniel's addition too
    price = db.Column(db.Float, nullable=False)
```

**Option 2: Keep only YOUR code** (rare)
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    age = db.Column(db.Integer)  # Only keep Tecla's
    price = db.Column(db.Float, nullable=False)
```

**Option 3: Keep only THEIR code** (rare)
```python
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False) 
    weight = db.Column(db.Float)  # Only keep Raniel's
    price = db.Column(db.Float, nullable=False)
```

**After deciding, finish the merge:**
```bash
# Save the file (with conflict markers removed!)
git add app/models/animal.py
git commit -m "Resolve merge conflict - kept both age and weight fields"
git push origin feature/animals
```

**Pro tip:** If unsure which to keep, ask in team chat or pair with the other person!

### Issue: "Someone committed directly to dev (skipped PR)"

**Your response:**
1. **Don't blame** - might be accident, probably confused which branch they were on

2. **Check the damage:**
```bash
git checkout dev
git pull origin dev
git log  # See recent commits - look for commits not from merged PRs
```

3. **Revert the commit:**
```bash
# Find the commit hash (looks like: a1b2c3d4)
git log --oneline  # Shows commits with short hashes

# Revert that specific commit (replace COMMIT_HASH with actual hash)
git revert COMMIT_HASH

# This creates a NEW commit that undoes the accidental one
# Git will open a text editor for commit message - save and close

# Push the revert
git push origin dev
```

4. **Help them recover their work:**
```bash
# Their code isn't lost! Help them move it to their feature branch:

# Get their accidentally committed code
git checkout dev
git log  # Find their commit, copy the hash

# Switch to their feature branch
git checkout feature/their-feature

# Cherry-pick their commit (brings just that commit to this branch)
git cherry-pick THEIR_COMMIT_HASH

# Push to their feature branch
git push origin feature/their-feature
```

5. **Remind team (kindly):**
   - "Always check which branch you're on: `git branch`"
   - "Before coding, make sure you see `* feature/your-feature`"
   - "Please always use feature branches and PRs - helps us catch bugs!"

6. **Prevent future accidents:**
   - Consider protecting the `dev` branch on GitHub:
     - Go to repo Settings → Branches → Add rule
     - Pattern: `dev`
     - Check "Require pull request before merging"
     - This prevents direct commits to dev (forces PRs)

### Issue: "Feature is taking way longer than expected"

**Your response:**
1. **Assess scope:**
   - Is it actually too hard?
   - Can we simplify? (MVP approach)
   - Can we split it into smaller pieces?

2. **Redistribute if needed:**
   - "Raniel, can you help Jonah with the payment endpoint?"
   - Linda (QA) can help with frontend if backend is done

3. **Adjust timeline:**
   - "Let's get Cart working without fancy filters first"
   - "We can add search in a future sprint"

---

## 📅 Weekly Planning

### Week 1 Goals (Jan 29 - Feb 4)

**By End of Week 1:**
- ✅ Auth feature complete and merged (YOU)
- ✅ Animals feature complete and merged (Tecla)
- 🔨 Cart feature at least 50% done (Raniel)
- 🔨 Orders backend endpoints started (Jonah)
- 📝 Test data seed script ready (Linda)

**Your Tasks:**
- Monday: Share TEAM_GUIDE.md, run kickoff meeting
- Tuesday-Wednesday: Review Animals PRs
- Thursday: Check-in 1-on-1 with each person (5 min each)
- Friday: Week 1 retro - what went well? what to improve?

### Week 2 Goals (Feb 5 - Feb 11)

**By End of Week 2:**
- ✅ ALL features complete and merged
- ✅ Cypress E2E tests passing
- ✅ No critical bugs
- ✅ Deployed to production (if required)
- 📊 Demo prepared

**Your Tasks:**
- Monday: Final push - everyone coding
- Tuesday: Code freeze - only bug fixes
- Wednesday: QA day - test everything together
- Thursday: Polish + demo prep
- Friday: DEMO DAY 🎉

---

## 🎤 Running Meetings

### Daily Standup (15 min)

**Format:**
```
[9:00 AM or whatever time you set]

"Good morning team! Let's do standup. Tecla, you first."

Tecla: "Yesterday I finished the GET animals endpoint. Today I'm working on the create endpoint. No blockers."

You: "Great! Raniel?"

Raniel: "Yesterday I set up the cart slice. Today I'm building the Cart component. I'm a bit stuck on how to get the current cart - can someone help after standup?"

You: "Sure, I can pair with you for 30 min after this. Jonah?"

[Continue for everyone]

"Alright team, good progress! Remember Animals PR is ready for review - please take a look today. Raniel and I will pair after this. Let's crush it! 💪"
```

**Tips:**
- Start on time, end on time
- Don't solve problems in standup - "let's discuss after"
- Keep energy positive
- Take notes on blockers

### Week 1 Retro (30 min - Friday of Week 1)

**Agenda:**
1. **What went well?** (10 min)
   - Everyone shares one good thing
   - Example: "PRs were reviewed fast!" "Pairing with Jonah helped a lot"

2. **What can improve?** (10 min)
   - Constructive feedback only
   - Example: "Need clearer commit messages" "More testing before PRs"

3. **Actions for Week 2** (10 min)
   - Pick 2-3 concrete changes
   - Example: "Use this commit message template" "Test checklist before PR"

**Your role:** Facilitate, don't dominate. Let team speak.

---

## 🔀 Branch Management Strategy

### Branches You Manage

**main branch:**
- Lock it - no one commits directly
- Only merge to main from dev at END of sprint
- This is your "production" code

**dev branch:**
- Integration branch
- Merge feature PRs here throughout sprint
- Test that features work together

**feature branches:**
- Team creates these
- They merge via PR to dev
- Delete after merge

**Your workflow:**
```bash
# Stay on dev most of the time
git checkout dev
git pull origin dev

# Test new features after merging
python run.py  # backend
npm run dev    # frontend

# At end of sprint, merge dev to main
git checkout main
git pull origin main
git merge dev
git push origin main
git tag v1.0.0  # Tag the release
git push origin v1.0.0
```

---

## 🎯 Keeping Team Motivated

### Celebrate Wins 🎉
- "🎉 Animals feature merged! Great work Tecla!"
- "We're 60% done with sprint - on track!"
- "All PRs reviewed in <24 hours this week - amazing team!"

### Recognize Effort
- "Jonah, great job on the error handling in that PR"
- "Linda, the test data script is super helpful"
- "Raniel, thanks for reviewing everyone's PRs so thoroughly"

### Be Honest About Challenges
- "We're behind on Orders - let's pair tomorrow to catch up"
- "This is hard, but we can do it"
- "I made this mistake too when learning - here's what helped me"

### Lead by Example
- Commit your own code regularly
- Review PRs promptly
- Respond to questions quickly
- Admit when you don't know something

---

## ✅ Pre-Demo Checklist (Day 13-14)

**Day before demo:**
- [ ] All features merged to dev
- [ ] No errors in backend logs
- [ ] No errors in frontend console
- [ ] Seed database with good demo data
- [ ] Test complete user journey (register → browse → cart → checkout → farmer confirms)
- [ ] Prepare talking points (who presents what)
- [ ] Practice demo run-through
- [ ] Have backup plan (screenshots if live demo fails)

**Demo day:**
- [ ] Deploy to production (if required) OR ensure local env works
- [ ] Clear browser cache
- [ ] Close unnecessary tabs
- [ ] Test one more time right before
- [ ] Have fun! 🎉

---

## 🆘 When to Ask for Help

You don't have to know everything! Ask your mentor/instructor when:

- **Technical blocker** - Team stuck on architectural decision
- **Team conflict** - Two people disagree on approach
- **Timeline concern** - Sprint falling seriously behind
- **Unclear requirements** - Not sure what mentor expects

**How to ask:**
- "We're debating two approaches for cart storage - can you advise?"
- "Team is behind schedule - should we cut features or extend timeline?"

---

## 📊 Tracking Progress (Optional but Helpful)

### GitHub Projects (Free)

Create a project board with columns:
- **Backlog** - All features
- **In Progress** - Being worked on
- **In Review** - PR submitted
- **Done** - Merged to dev

Move cards as team progresses. Visual progress motivator!

### Simple Spreadsheet

| Feature | Owner | Status | PR Link | Merged Date |
|---------|-------|--------|---------|-------------|
| Auth | Vanessa | Testing | #1 | - |
| Animals | Tecla | In Progress | - | - |
| Cart | Raniel | Not Started | - | - |
| Orders | Jonah | Not Started | - | - |
| QA | Linda | In Progress | - | - |

Update daily in standup.

---

## 🎓 Your Learning Opportunity

You're not just building an app - you're learning to LEAD. Skills you're gaining:

- **Project management** - Planning, tracking, adjusting
- **Code review** - Reading others' code, giving feedback
- **Communication** - Running meetings, unblocking team
- **Technical leadership** - Making architectural decisions
- **Mentorship** - Helping teammates level up

These skills are HUGE for your career! 🚀

---

## 💡 Pro Tips

### Time Management
- **Block focus time** - 2 hours to work on YOUR feature
- **Block review time** - 1 hour daily for PR reviews
- **Be available** - But not 24/7, set boundaries

### Communication
- **Overcommunicate** - "Merged Animals to dev, please pull latest!"
- **Be specific** - Not "good job", but "great error handling in that function"
- **Stay positive** - Even when stressed

### Code Quality
- **Same standards for everyone** - Don't let bad code through because you're friends
- **But be encouraging** - "This works, but here's a better way"

### Self Care
- **You can't pour from empty cup**
- Take breaks
- Ask for help
- It's okay to not know everything

---

## 📋 Your Week-by-Week Checklist

### Week 1
- [x] Share TEAM_GUIDE.md with team
- [x] Run kickoff meeting - explain workflow
- [ ] Test and commit your Auth feature
- [ ] Review Animals PR (Tecla)
- [ ] Review any other PRs within 24 hours
- [ ] Run daily standups
- [ ] Friday retro

### Week 2
- [ ] Review Cart PR (Raniel)
- [ ] Review Orders PR (Jonah)
- [ ] Review QA/Testing work (Linda)
- [ ] Merge all features to dev
- [ ] Integration testing
- [ ] Bug fixes
- [ ] Merge dev to main
- [ ] Demo prep
- [ ] DEMO DAY 🎉

---

## 🎉 Final Thoughts

**You've got this!** Leadership is hard, but you're doing great by being prepared.

**Remember:**
- Trust your team
- Communicate clearly
- Review code thoroughly
- Stay organized
- Celebrate wins
- Learn from mistakes

**Your team is counting on you, but they also want to help you succeed. You're in this TOGETHER.** 🤝

---

**Questions? Revisit this guide. Still stuck? Ask your mentor.**

**Now go lead your team to success! 🚀**
