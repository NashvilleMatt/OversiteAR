#!/usr/bin/env python3
"""Builds index.html for the Oversite AR dashboard. Run: python3 build.py"""
from html import escape as e

AS_OF = "October 27, 2026"

SHIELD = ('<svg class="shield" viewBox="26 0 100 67" aria-hidden="true">'
          '<path fill="#e0a100" d="M67,0h21.94v7.25c0,.09,0,.17,0,.26v7.95c0,1.07-.62,2.14-1.7,2.76l-7.88,4.59c-.93.46-1.86.46-2.78,0l-7.88-4.59c-1.08-.46-1.7-1.53-1.7-2.76v-7.7h0V0Z"/>'
          '<path fill="#e0a100" d="M93.26,17.12V5.14c14.63,5.99,24.74,20.13,24.74,36.87l-8.56,4.15c-1.4.61-2.33,2-2.49,3.53l-1.09,8.6c-18.52-3.23-37.04-3.23-54.93-.15l-1.09-8.6c-.16-1.54-1.09-2.92-2.49-3.53l-10.11-4.92c.47-16.29,10.58-30.11,24.9-35.95v11.98c0,2.3,1.24,4.46,3.42,5.53l9.34,4.61c.93.46,1.87.61,2.8.61s1.87-.15,2.8-.61l9.34-4.61c2.18-1.08,3.42-3.23,3.42-5.53Z"/>'
          '</svg>')

# status: good | attention | hold
CUSTOMERS = [
    dict(slug="collier", name="Collier Engineering", logo="collier", status="hold",
         seats="42 / 41", seats_note="40 on renewal", billing="Annual", term="2027 renewal due 10/29",
         open="$87,580.50", past="$0",
         notes=["Open COLLIERTN-0002 is $87,580.50 (40 seats x $1,995 + tax), due 10/29, not past due.",
                "Matt is reworking the invoice with a prepay discount of about 10% on top of the annual rate.",
                "Seat count still open: 42 active in Oversite (Max Hammer added 10/16) vs 40 on the renewal."],
         next=("Matt", "Settle discount and seat count, then replace COLLIERTN-0002.")),
    dict(slug="lda", name="LDA Engineering", logo="lda", status="hold",
         seats="10 / 9", seats_note="", billing="Annual", term="Paid through 9/23/2027",
         open="$0", past="$0",
         notes=["Paid LDATN-0001 in full: $19,705.61 by card.",
                "Brenden Clark (admin) was added 10/19. Catch-up would be $1,852.89, or $2,033.55 with tax.",
                "Hard to collect from. Get them under contract before any more billing."],
         next=("Matt", "Contract first. Hold the catch-up until it is signed.")),
    dict(slug="ttl", name="TTL", logo="ttl", status="good",
         seats="8 / 8", seats_note="", billing="Annual", term="Term to 7/31/2027",
         open="$0", past="$0",
         notes=["Paid in full by two checks: $5,209.45 (9/2) and $16,975.86 (9/14)."],
         next=None),
    dict(slug="volkert", name="Volkert", logo="volkert", status="attention",
         seats="27 / 20", seats_note="across 3 entities", billing="Annual + monthly", term="Brentwood term ends 11/30/2026",
         open="$10,240.39", past="$8,169.60",
         notes=["Three Stripe entities with very different health. Virginia Beach is the problem account.",
                "Customer is flagged delinquent in Stripe because of Virginia Beach."],
         subs=[
             ("Brentwood TN", "18 / 12", "Annual", "$0",
              "Nothing open. Catch-up for 6 unbilled seats est. $3,760 to $4,370 before tax. Dec 1 renewal at 18 seats is $32,279.67 with tax. Send early."),
             ("Springfield VA", "5 / 5", "Annual", "$5,040.39",
              "VOLKVA-0004 $3,419.60 is 6 days late. VOLKVA-0006 $1,620.79 due 11/5. A $3,420 check landed 10/8, likely meant for 0004."),
             ("Virginia Beach", "4 / 3", "Monthly", "$5,200.00",
              "$4,750 past due: 0001 $3,850 (48 days), 0002 $450 (43 days), 0003 $450 (12 days). 0007 $450 due 11/14. Joseph Harvey (7/22) may be unbilled, about $561."),
         ],
         next=("Marissa", "Confirm what the $3,420 check covered, work the Virginia Beach collections, send the Brentwood renewal early.")),
    dict(slug="tlm", name="TLM", logo="tlm", status="good",
         seats="7 / 7", seats_note="", billing="Monthly autopay", term="Next charge 11/13",
         open="$0", past="$0",
         notes=["Autopay at $1,152.38 a month. Last charge paid 10/19."],
         next=None),
    dict(slug="asa", name="ASA Engineering", logo="asa", status="good",
         seats="2 / 2", seats_note="", billing="Annual", term="Term ends 2/11/2027",
         open="$0", past="$0",
         notes=["Paid ASATN-0001, $6,663.66, by check on 9/14.",
                "No subscription in Stripe. The February renewal needs a manual invoice."],
         next=("Matt", "Calendar the February renewal invoice.")),
    dict(slug="hdr", name="HDR", logo="hdr", status="good",
         seats="6 / 6", seats_note="one shared seat approved", billing="Annual", term="Paid 10/21",
         open="$0", past="$0",
         notes=["HDRTN-0001, $12,067.60, paid by ACH on 10/21 and marked paid in Stripe. It landed about 39 days late.",
                "A stale $1,876.73 draft invoice is still in Stripe and should be voided."],
         next=("Matt", "Void the stale draft.")),
    dict(slug="hmb", name="HMB Professional Engineers", logo="hmb", status="attention",
         seats="8 / 8", seats_note="", billing="Monthly (ACH)", term="Cycle renews on the 7th",
         open="$1,427.78", past="$0",
         notes=["HMBTN-0002 ($1,646.25) is paid. Open HMBTN-0003 is $1,427.78, due 11/6.",
                "0003 includes a one seat bump (10 to 11 on 9/15, which lines up with Jared Tuttle's account on 9/14) worth $100.95 net, then 8 seats for Oct 7 to Nov 7 at $1,200.",
                "Four other users are inactive and Oversite does not store removal dates. We need a policy on seats removed mid-cycle.",
                "TUN2DAXI-0004 ($329.25, Dec 2025) is probably stale and needs an older bank export to confirm."],
         next=("Marissa", "Pick the mid-cycle removal policy, then Matt reissues 0003 if needed.")),
    dict(slug="fisher-arnold", name="Fisher Arnold", logo="fisher-arnold", status="good",
         seats="2 / 2", seats_note="", billing="Annual", term="Year two starts around 5/2027",
         open="$0", past="$0",
         notes=["Year one UUIRUFD4-0003, $6,497.20, paid by paper check deposited 5/29.",
                "The premature year two invoice (UUIRUFD4-0002, $3,753.45) was voided 10/27.",
                "No subscription yet. Year two needs an invoice created before May."],
         next=("Matt", "Set up year two billing before 5/2027.")),
    dict(slug="egis", name="Egis (Lochner)", logo="egis", status="good",
         seats="5 / 5", seats_note="", billing="Annual", term="8/3/2026 to 8/3/2027",
         open="$0", past="$0",
         notes=["Paid LOCHTN-0001, $10,250.65, by ACH on 9/3."],
         next=None),
    dict(slug="chen-moore", name="Chen Moore and Associates", logo="chen-moore", status="attention",
         seats="7 / 7", seats_note="", billing="Monthly", term="Next invoice 10/28 at 7 seats ($1,050)",
         open="$1,925.00", past="$225.00",
         notes=["CHENFL-0003 ($225, trial rate) is 32 days late. CHENFL-0005 ($1,700, second half of implementation plus 3 seats) is due 10/28.",
                "Four seats were added after the trial (2 on 9/30, 2 on 10/15). Catch-up is $410.",
                "Flagged delinquent in Stripe. A call to walk through billing is the better move than another reminder."],
         next=("Marissa", "Offer a call, then settle monthly vs annual going forward.")),
    dict(slug="pape-dawson", name="Pape-Dawson Engineers", logo="pape-dawson", status="good",
         seats="3 / 3", seats_note="", billing="Annual", term="Through 7/2/2027",
         open="$0", past="$0",
         notes=["Paid $8,373.93 by ACH on 8/19.",
                "The San Antonio sandbox company has one active admin that is not billed."],
         next=("Marissa", "Decide whether the sandbox admin needs a seat.")),
    dict(slug="basis", name="Basis Partners", logo="basis", status="good",
         seats="5 / 6", seats_note="billed one over", billing="Monthly", term="Next invoice 11/11",
         open="$0", past="$0",
         notes=["Paid $3,400 (9/23) and $900 (10/20).",
                "Michael Gillen has two accounts, which is probably why the billed count runs one high."],
         next=("Marissa", "Confirm the seat count with Basis.")),
    dict(slug="gha", name="Gewalt Hamilton Associates", logo="gha", status="attention",
         seats="5 / 0", seats_note="not in Stripe yet", billing="3-month trial", term="Agreement signed 10/13",
         open="$0", past="$0",
         notes=["Newest customer. Signed a 3-month trial for 3 users, but 5 are already active in Oversite (latest added 10/20).",
                "No Stripe customer exists and no invoice has gone out. Expected trial invoice is about $1,700 before tax: 50% of implementation plus monthly user fees.",
                "Bill to ap@gha-engineers.com, optional PO KDM20261012. Contact: Dave Marquardt."],
         next=("Marissa", "Confirm terms and onboarding date so Matt can create the customer and invoice.")),
]

STATUS_LABEL = {"good": "Good standing", "attention": "Needs attention", "hold": "On hold"}

# Where the open balance sits (sums to $101,173.67)
OPEN_BY = [("Collier", 87580.50), ("Volkert", 10240.39), ("Chen Moore", 1925.00), ("HMB", 1427.78)]
OPEN_TOTAL = sum(v for _, v in OPEN_BY)
assert round(OPEN_TOTAL, 2) == 101173.67, OPEN_TOTAL
PAST_TOTAL = 4750.00 + 3419.60 + 225.00
assert round(PAST_TOTAL, 2) == 8394.60
assert round(OPEN_TOTAL - PAST_TOTAL, 2) == 92779.07

n_good = sum(c["status"] == "good" for c in CUSTOMERS)
n_att = sum(c["status"] == "attention" for c in CUSTOMERS)
n_hold = sum(c["status"] == "hold" for c in CUSTOMERS)
assert len(CUSTOMERS) == 14

TASKS = [
    ("Matt", "Collier: rework COLLIERTN-0002 with the prepay discount and final seat count", "Due 10/29", "Human"),
    ("Marissa", "Volkert Virginia Beach: collect $4,750 past due (oldest 48 days)", "This week", "Cowork can draft the follow-up"),
    ("Marissa", "Volkert Springfield: ask whether the 10/8 $3,420 check was for VOLKVA-0004", "This week", "Cowork can draft the email"),
    ("Marissa", "Chen Moore: offer a billing call, settle monthly vs annual", "Before 10/28", "Cowork can draft talking points"),
    ("Marissa", "HMB: choose mid-cycle seat removal policy", "This week", "Decision"),
    ("Matt", "HMB: reissue HMBTN-0003 if the policy changes the math", "After decision", "Human, Stripe"),
    ("Matt", "Volkert Brentwood: catch-up and Dec 1 renewal (18 seats, $32,279.67 with tax)", "Send by mid Nov", "Cowork can draft the proration note"),
    ("Matt", "LDA: sign contract first, then $2,033.55 catch-up", "On hold", "Human"),
    ("Marissa", "GHA: confirm terms and onboarding date, then trial invoice (about $1,700 pre-tax)", "This week", "Cowork can draft the invoice note"),
    ("Matt", "Void four stale draft invoices in Stripe (HDR, HMB, Volkert TN, test)", "Anytime", "Human, Stripe"),
    ("Matt", "Send Pilot the non-revenue deposits: IRS $2,224.87, Launch Tennessee $2,000, SiteGround credit $359.88", "This week", "Cowork can draft the note"),
    ("Matt", "Calendar manual renewals: ASA (Feb 2027), Fisher Arnold (May 2027)", "Later", "Cowork can draft reminders"),
]


def money(v):
    return "${:,.2f}".format(v)


def card(c):
    st = c["status"]
    seats_note = f' <span class="muted">({e(c["seats_note"])})</span>' if c["seats_note"] else ""
    past_cls = " warn" if c["past"] not in ("$0", "$0.00") else ""
    notes = "".join(f"<li>{e(n)}</li>" for n in c["notes"])
    subs = ""
    if c.get("subs"):
        rows = "".join(
            f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(cc)}</td><td class="num">{e(d)}</td></tr>'
            f'<tr class="subnote"><td colspan="4">{e(f)}</td></tr>'
            for a, b, cc, d, f in c["subs"])
        subs = ('<table class="subs"><thead><tr><th>Entity</th><th>Seats</th><th>Billing</th><th class="num">Open</th></tr></thead>'
                f"<tbody>{rows}</tbody></table>")
    nxt = ""
    if c["next"]:
        who, what = c["next"]
        nxt = f'<div class="next"><span class="owner {who.lower()}">{e(who)}</span><span>{e(what)}</span></div>'
    return f'''
<article class="card" data-status="{st}" id="{c["slug"]}">
  <div class="logo-wrap"><img src="logos/{c["logo"]}.png" alt="{e(c["name"])} logo"></div>
  <div class="card-body">
    <div class="card-head"><h3>{e(c["name"])}</h3><span class="pill {st}">{STATUS_LABEL[st]}</span></div>
    <dl class="stats">
      <div><dt>Seats (Oversite / Stripe)</dt><dd>{e(c["seats"])}{seats_note}</dd></div>
      <div><dt>Billing</dt><dd>{e(c["billing"])}</dd></div>
      <div><dt>Open balance</dt><dd class="num">{e(c["open"])}</dd></div>
      <div><dt>Past due</dt><dd class="num{past_cls}">{e(c["past"])}</dd></div>
    </dl>
    <p class="term">{e(c["term"])}</p>
    <ul class="notes">{notes}</ul>
    {subs}
    {nxt}
  </div>
</article>'''


def bars():
    mx = OPEN_BY[0][1]
    out = []
    for name, v in OPEN_BY:
        w = max(v / mx * 100, 1.2)
        pct = v / OPEN_TOTAL * 100
        out.append(f'<div class="bar-row"><span class="bar-label">{e(name)}</span>'
                   f'<span class="bar-track"><span class="bar-fill" style="width:{w:.1f}%"></span></span>'
                   f'<span class="bar-val num">{money(v)} <em>{pct:.1f}%</em></span></div>')
    return "".join(out)


def tasks():
    rows = "".join(
        f'<tr><td><span class="owner {o.lower()}">{o}</span></td><td>{e(t)}</td><td>{e(d)}</td><td class="muted">{e(k)}</td></tr>'
        for o, t, d, k in TASKS)
    return ('<table class="tasks"><thead><tr><th>Owner</th><th>Task</th><th>Timing</th><th>Who can do it</th></tr></thead>'
            f"<tbody>{rows}</tbody></table>")


def radio(name, opts):
    return "".join(
        f'<label class="opt"><input type="radio" name="{name}" value="{e(o)}"> <span>{e(o)}</span></label>' for o in opts)


def form(fid, title, intro, fields_html, subject):
    return f'''
<section class="qcard" id="q-{fid}">
  <h3>{e(title)}</h3>
  <p class="intro">{e(intro)}</p>
  <form name="{fid}" method="POST" action="/" data-netlify="true" netlify-honeypot="bot-field" class="qform">
    <input type="hidden" name="form-name" value="{fid}">
    <input type="hidden" name="subject" value="{e(subject)} (%{{submissionId}})">
    <p class="hp"><label>Leave blank <input name="bot-field"></label></p>
    {fields_html}
    <div class="row"><label class="fl">Your name<input type="text" name="name" value="Marissa" autocomplete="name"></label></div>
    <button type="submit">Send answers to Matt</button>
    <p class="status" role="status" aria-live="polite"></p>
  </form>
</section>'''


def q(label, inner):
    return f'<fieldset class="q"><legend>{e(label)}</legend>{inner}</fieldset>'


def ta(name, ph="Anything else we should know"):
    return f'<label class="fl">Notes<textarea name="{name}" rows="3" placeholder="{e(ph)}"></textarea></label>'


FORMS = [
    form("hmb", "HMB: seats added and removed",
         "HMB went from 10 seats to 11 on 9/15, then back to 8 on 10/7. We need a policy before 0003 goes out.",
         q("When a customer drops seats mid-cycle, what do we do?",
           radio("removal_policy", [
               "No credit. The lower count starts at the next renewal (send 0003 as issued)",
               "Credit removed seats from the removal date (reissue 0003)",
               "Case by case, I will tell you for HMB"])) +
         q("Do you know when the four inactive users were removed?",
           ta("removal_dates", "Names and dates if you know them, or who at HMB could confirm")) +
         q("TUN2DAXI-0004 ($329.25, Dec 2025). Void it?",
           radio("void_0004", ["Yes, void it", "No, they still owe it", "Not sure, check an older bank export"])),
         "AR answers: HMB"),
    form("chen-moore", "Chen Moore: billing path and a call",
         "Chen Moore is on monthly while they add users. Still owed: the $225 trial invoice and the second half of implementation ($1,700 due 10/28).",
         q("How should billing work going forward?",
           radio("billing_path", [
               "Monthly for now, move to annual once user count settles",
               "Stay monthly",
               "Move to annual now"])) +
         q("If annual later, roughly when should we revisit?",
           '<label class="fl">Timing<input type="text" name="revisit" placeholder="For example, after January"></label>') +
         q("Who offers the call to walk through the invoices?",
           radio("call", ["Marissa will call", "Matt will call", "Email only for now"])) +
         q("The $410 catch-up for the four added seats",
           radio("catchup", ["Bill it now as its own invoice", "Roll it into the next subscription invoice"])) +
         ta("notes"),
         "AR answers: Chen Moore"),
    form("volkert", "Volkert: three entities, three questions",
         "Brentwood is healthy but under-billed, Springfield has a payment to match, and Virginia Beach is well past due.",
         q("Was the 10/8 check for $3,420 meant for VOLKVA-0004 ($3,419.60)?",
           radio("check_3420", ["Yes, apply it to 0004", "No, it was for something else", "Not sure, ask Volkert for the remittance detail"])) +
         q("How do we handle Virginia Beach ($4,750 past due)?",
           radio("vb_collections", [
               "Call their AP contact",
               "Email reminder with all four invoices attached",
               "Raise it in the Brentwood renewal conversation"])) +
         q("Brentwood renewal and catch-up: when should it go out?",
           '<label class="fl">Target send date<input type="text" name="brentwood_date" placeholder="For example, Nov 10"></label>') +
         ta("notes", "Contacts at Volkert, anything you have heard from them"),
         "AR answers: Volkert"),
    form("gha", "GHA: build the trial invoice?",
         "Signed 10/13 for a 3 user, 3 month trial. Five users are active. No Stripe customer exists yet.",
         q("Go ahead and build the trial invoice now?",
           radio("go_ahead", ["Yes, build it now", "Wait until onboarding is on the calendar"])) +
         q("Onboarding date",
           '<label class="fl">Date<input type="text" name="onboarding_date" placeholder="If scheduled"></label>') +
         q("Bill for 3 users (per agreement) or 5 (actually active)?",
           radio("billed_users", ["3 per the agreement", "5 as active", "Ask Dave Marquardt first"])) +
         q("Billing details",
           '<label class="fl">PO number and AP email<input type="text" name="po" value="PO KDM20261012, ap@gha-engineers.com"></label>') +
         ta("notes"),
         "AR answers: GHA"),
    form("general", "Anything else",
         "Questions, corrections, or customers we missed.",
         ta("notes", "Type anything here"),
         "AR answers: general"),
]

CSS = r'''
:root{--bg:#191d20;--card:#21272b;--card-h:#282f34;--bd:#333a3f;--bd2:#444d54;--tx:#b3bac1;--mut:#7d868e;--br:#e8eaed;--hd:#f2f3f5;--gold:#e0a100;--gold-l:#f0b830;--glow:rgba(224,161,0,.15);--ok:#6fae8a}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--tx);font:17px/1.65 'Source Serif 4',Georgia,serif;-webkit-font-smoothing:antialiased}
h1,h2,h3,.pill,.owner,dt,th,button,legend,.label,.kpi b,.filters button,.bar-label{font-family:'Outfit',system-ui,sans-serif}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
header.top{border-bottom:1px solid var(--bd);background:rgba(25,29,32,.85);backdrop-filter:blur(10px);position:sticky;top:0;z-index:10}
header.top .wrap{display:flex;align-items:center;gap:14px;height:64px}
.shield{height:34px;width:auto}
.brand{font:600 18px 'Outfit',sans-serif;color:var(--hd);letter-spacing:.2px}
.brand small{display:block;font:400 12px 'Outfit',sans-serif;color:var(--mut);letter-spacing:.4px}
nav{margin-left:auto;display:flex;gap:18px;font:500 14px 'Outfit',sans-serif}
nav a{color:var(--tx);text-decoration:none}nav a:hover{color:var(--gold-l)}
.hero{padding:56px 0 24px}
.hero h1{margin:0 0 8px;font-weight:700;font-size:clamp(30px,5vw,46px);line-height:1.1;color:var(--hd);letter-spacing:-.5px}
.hero p{margin:0;max-width:640px;color:var(--tx)}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:32px 0}
.kpi{min-width:0;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:20px 22px}
.kpi .label{font-size:12px;letter-spacing:.8px;text-transform:uppercase;color:var(--mut)}
.kpi b{display:block;font-size:30px;font-weight:600;color:var(--hd);margin-top:4px;font-variant-numeric:tabular-nums}
.kpi.gold b{color:var(--gold)}
.kpi small{display:block;color:var(--mut);font-size:14px;margin-top:2px}
.panel{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:26px 28px;margin-bottom:24px}
.panel h2{margin:0 0 4px;font-size:20px;color:var(--hd);font-weight:600}
.panel .sub{margin:0 0 18px;color:var(--mut);font-size:15px}
.bar-row{display:grid;grid-template-columns:110px 1fr 200px;gap:14px;align-items:center;margin:10px 0}
.bar-label{font-size:14px;color:var(--br);font-weight:500}
.bar-track{height:12px;background:#171b1e;border-radius:6px;overflow:hidden}
.bar-fill{display:block;height:100%;background:var(--gold);border-radius:6px}
.bar-val{text-align:right;color:var(--br);font:500 15px 'Outfit',sans-serif}
.bar-val em{font-style:normal;color:var(--mut);margin-left:6px}
.num{font-variant-numeric:tabular-nums}
section.block{padding:40px 0 8px}
section.block>h2{font-size:28px;color:var(--hd);margin:0 0 6px;font-weight:700}
section.block>p.lead{margin:0 0 22px;color:var(--mut)}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 24px}
.filters button{background:transparent;color:var(--tx);border:1px solid var(--bd2);border-radius:8px;padding:8px 14px;font-size:14px;font-weight:500;cursor:pointer}
.filters button:hover{border-color:var(--gold);color:var(--hd)}
.filters button[aria-pressed=true]{background:var(--gold);border-color:var(--gold);color:#20272a;font-weight:600}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;overflow:hidden;display:flex;flex-direction:column;scroll-margin-top:84px}
.card:hover{background:var(--card-h)}
.card[hidden]{display:none}
.logo-wrap{height:104px;display:flex;align-items:center;padding:0 28px;background:#1b2023;border-bottom:1px solid var(--bd)}
.logo-wrap img{max-height:54px;max-width:78%;width:auto;height:auto;object-fit:contain;opacity:.95}
.card-body{padding:22px 26px 24px;display:flex;flex-direction:column;gap:12px;flex:1}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.card-head h3{margin:0;font-size:20px;font-weight:600;color:var(--hd);line-height:1.25}
.pill{font-size:11px;font-weight:600;letter-spacing:.8px;text-transform:uppercase;padding:5px 10px;border-radius:8px;white-space:nowrap;border:1px solid var(--bd2);color:var(--tx)}
.pill::before{content:"";display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:7px;vertical-align:1px;background:var(--mut)}
.pill.good::before{background:var(--ok)}
.pill.attention{background:var(--glow);border-color:rgba(224,161,0,.5);color:var(--gold-l)}
.pill.attention::before{background:var(--gold)}
.pill.hold::before{background:transparent;border:1.5px solid var(--mut)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin:4px 0 0}
.stats dt{font-size:11px;letter-spacing:.7px;text-transform:uppercase;color:var(--mut)}
.stats dd{margin:2px 0 0;color:var(--br);font:500 16px 'Outfit',sans-serif}
.stats dd.warn{color:var(--gold)}
.muted{color:var(--mut);font-weight:400}
.term{margin:0;font-size:14px;color:var(--mut)}
.notes{margin:0;padding-left:18px;font-size:15px;line-height:1.55}
.notes li{margin:5px 0}
.next{display:flex;gap:10px;align-items:flex-start;margin-top:auto;padding:12px 14px;border-left:3px solid var(--gold);background:var(--glow);border-radius:0 8px 8px 0;font-size:15px;color:var(--br)}
.owner{display:inline-block;font-size:11px;font-weight:600;letter-spacing:.7px;text-transform:uppercase;padding:3px 8px;border-radius:6px;background:#2d353a;color:var(--br);border:1px solid var(--bd2);white-space:nowrap;line-height:1.5}
table{width:100%;border-collapse:collapse}
.subs{font-size:14px;margin-top:2px}
.subs th,.subs td{padding:6px 8px;text-align:left;border-bottom:1px solid var(--bd);vertical-align:top}
.subs thead th{font:500 11px 'Outfit',sans-serif;letter-spacing:.7px;text-transform:uppercase;color:var(--mut)}
.subs th[scope=row]{font:500 14px 'Outfit',sans-serif;color:var(--br)}
.subs .num,.tasks .num{text-align:right}
.subs .subnote td{color:var(--tx);font-size:13.5px;line-height:1.5;padding-top:0;padding-bottom:10px}
.tasks{font-size:15px}
.tasks th{font:500 11px 'Outfit',sans-serif;letter-spacing:.7px;text-transform:uppercase;color:var(--mut);text-align:left;padding:8px 10px;border-bottom:1px solid var(--bd2)}
.tasks td{padding:11px 10px;border-bottom:1px solid var(--bd);vertical-align:top}
.tasks td:nth-child(3){white-space:nowrap;color:var(--br)}
.qgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}
.qcard{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:26px 28px;scroll-margin-top:84px}
.qcard h3{margin:0 0 4px;font-size:20px;font-weight:600;color:var(--hd)}
.qcard .intro{margin:0 0 16px;font-size:15px;color:var(--mut)}
.q{border:0;margin:0 0 16px;padding:0}
.q legend{padding:0;margin-bottom:6px;font-size:15px;font-weight:500;color:var(--br)}
.opt{display:flex;gap:10px;align-items:flex-start;padding:9px 12px;border:1px solid var(--bd2);border-radius:8px;margin:6px 0;cursor:pointer;font-size:15px;line-height:1.45}
.opt:hover{border-color:var(--gold)}
.opt input{margin-top:5px;accent-color:var(--gold)}
.fl{display:block;font:500 13px 'Outfit',sans-serif;color:var(--mut);letter-spacing:.3px}
.fl input,.fl textarea{display:block;width:100%;margin-top:5px;background:#171b1e;color:var(--br);border:1px solid var(--bd2);border-radius:8px;padding:10px 12px;font:16px 'Source Serif 4',Georgia,serif}
.fl input:focus,.fl textarea:focus,.opt:focus-within{outline:2px solid var(--gold);outline-offset:1px}
.row{margin:0 0 16px}.qform>.fl,.q .fl{margin-bottom:6px}.q>.fl:last-child{margin-bottom:0}.qform .row .fl{margin-bottom:0}
button[type=submit]{background:var(--gold);color:#20272a;border:0;border-radius:6px;padding:12px 20px;font-size:15px;font-weight:600;cursor:pointer}
button[type=submit]:hover{background:var(--gold-l)}
button[type=submit]:disabled{opacity:.6;cursor:wait}
.status{margin:12px 0 0;font:500 14px 'Outfit',sans-serif;min-height:1.2em}
.status.ok{color:var(--ok)}.status.err{color:var(--gold-l)}
.hp{position:absolute;left:-9999px;height:0;overflow:hidden}
footer{margin-top:64px;padding:28px 0 48px;border-top:1px solid var(--bd);font:14px 'Outfit',sans-serif;color:var(--mut)}
footer p{margin:4px 0}
@media(max-width:860px){.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.grid,.qgrid{grid-template-columns:1fr}nav{display:none}.bar-row{grid-template-columns:90px 1fr;}.bar-val{grid-column:1/-1;text-align:left;margin-top:-4px}}
@media(max-width:520px){.wrap{padding:0 16px}.kpis{gap:12px}.kpi b{font-size:21px}.kpi{padding:16px}.panel,.qcard{padding:20px}.card-body{padding:18px}.tasks thead{display:none}.tasks tr{display:block;padding:10px 0;border-bottom:1px solid var(--bd)}.tasks td{display:block;border:0;padding:3px 0}.tasks td:nth-child(3){white-space:normal}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''

JS = r'''
(function(){
  var btns=document.querySelectorAll('.filters button'),cards=document.querySelectorAll('.card');
  btns.forEach(function(b){b.addEventListener('click',function(){
    btns.forEach(function(x){x.setAttribute('aria-pressed','false')});
    b.setAttribute('aria-pressed','true');
    var f=b.getAttribute('data-f');
    cards.forEach(function(c){c.hidden=(f!=='all'&&c.getAttribute('data-status')!==f)});
  })});
  document.querySelectorAll('form.qform').forEach(function(form){
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var s=form.querySelector('.status'),btn=form.querySelector('button[type=submit]');
      btn.disabled=true;s.className='status';s.textContent='Sending...';
      fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},
        body:new URLSearchParams(new FormData(form)).toString()})
      .then(function(r){if(!r.ok)throw new Error(r.status);s.className='status ok';s.textContent='Sent. Matt has your answers.';btn.textContent='Send again'})
      .catch(function(){s.className='status err';s.textContent='That did not go through. Try again, or reply to Matt directly.'})
      .then(function(){btn.disabled=false});
    });
  });
})();
'''


def page():
    cards = "".join(card(c) for c in CUSTOMERS)
    fav = "data:image/svg+xml," + (
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='26 0 100 67'%3E%3Cpath fill='%23e0a100' d='M93.26,17.12V5.14c14.63,5.99,24.74,20.13,24.74,36.87l-8.56,4.15c-1.4.61-2.33,2-2.49,3.53l-1.09,8.6c-18.52-3.23-37.04-3.23-54.93-.15l-1.09-8.6c-.16-1.54-1.09-2.92-2.49-3.53l-10.11-4.92c.47-16.29,10.58-30.11,24.9-35.95v11.98c0,2.3,1.24,4.46,3.42,5.53l9.34,4.61c.93.46,1.87.61,2.8.61s1.87-.15,2.8-.61l9.34-4.61c2.18-1.08,3.42-3.23,3.42-5.53Z'/%3E%3C/svg%3E")
    qforms = "".join(FORMS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Oversite AR Review</title>
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">{SHIELD}<div class="brand">Oversite<small>Accounts receivable review</small></div>
<nav><a href="#customers">Customers</a><a href="#actions">Action list</a><a href="#questions">Questions</a></nav></div></header>
<main class="wrap">
<div class="hero">
<h1>14 customers. One clear picture.</h1>
<p>Status of every customer under contract as of {AS_OF}, built from Stripe, the Oversite database, and the PNFP bank deposits. Questions that need your call are at the bottom.</p>
</div>

<div class="kpis">
<div class="kpi gold"><span class="label">Open balance</span><b>{money(OPEN_TOTAL)}</b><small>Stripe, after clean-up</small></div>
<div class="kpi"><span class="label">Past due</span><b>{money(PAST_TOTAL)}</b><small>Volkert and Chen Moore</small></div>
<div class="kpi"><span class="label">Not yet due</span><b>{money(OPEN_TOTAL - PAST_TOTAL)}</b><small>Mostly Collier, due 10/29</small></div>
<div class="kpi"><span class="label">Customers</span><b>{len(CUSTOMERS)}</b><small>{n_good} good, {n_att} attention, {n_hold} on hold</small></div>
</div>

<div class="panel">
<h2>Where the open balance sits</h2>
<p class="sub">Collier alone is most of it. Everything else is small, but Volkert Virginia Beach is the oldest.</p>
{bars()}
<p class="sub" style="margin:14px 0 0">Excludes HMB TUN2DAXI-0004 ($329.25), which is likely stale and unverified, and unbilled catch-ups.</p>
</div>

<section class="block" id="customers">
<h2>Customers</h2>
<p class="lead">Seats are active users in Oversite, then seats billed in Stripe. Viewers are not counted.</p>
<div class="filters" role="group" aria-label="Filter customers">
<button type="button" data-f="all" aria-pressed="true">All {len(CUSTOMERS)}</button>
<button type="button" data-f="attention" aria-pressed="false">Needs attention {n_att}</button>
<button type="button" data-f="hold" aria-pressed="false">On hold {n_hold}</button>
<button type="button" data-f="good" aria-pressed="false">Good standing {n_good}</button>
</div>
<div class="grid">{cards}</div>
</section>

<section class="block" id="actions">
<h2>Action list</h2>
<p class="lead">In priority order.</p>
<div class="panel">{tasks()}</div>
</section>

<section class="block" id="questions">
<h2>Questions for Marissa</h2>
<p class="lead">Quick answers are fine. Each one goes straight to Matt.</p>
<div class="qgrid">{qforms}</div>
</section>
</main>
<footer><div class="wrap"><p>Golden Spike Technologies, Inc. (Oversite). Internal, not for distribution.</p>
<p>Sources: Stripe, Oversite production database, PNFP bank deposits through 10/27/2026. Seat counts and balances are a snapshot and will drift.</p></div></footer>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    open("index.html", "w").write(page())
    print("wrote index.html")
