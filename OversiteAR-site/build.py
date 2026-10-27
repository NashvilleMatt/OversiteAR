#!/usr/bin/env python3
"""Builds index.html for the Oversite AR dashboard. Run: python3 build.py"""
from html import escape as e

AS_OF = "October 27, 2026"


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


# ---- Brand assets (Oversite Brand & Style Guide v2.0) ----
HAT = ('<path d="M67,0h21.94v7.25c0,.09,0,.17,0,.26v7.95c0,1.07-.62,2.14-1.7,2.76l-7.88,4.59c-.93.46-1.86.46-2.78,0l-7.88-4.59c-1.08-.46-1.7-1.53-1.7-2.76v-7.7h0V0Z"/>'
       '<path d="M93.26,17.12V5.14c14.63,5.99,24.74,20.13,24.74,36.87l-8.56,4.15c-1.4.61-2.33,2-2.49,3.53l-1.09,8.6c-18.52-3.23-37.04-3.23-54.93-.15l-1.09-8.6c-.16-1.54-1.09-2.92-2.49-3.53l-10.11-4.92c.47-16.29,10.58-30.11,24.9-35.95v11.98c0,2.3,1.24,4.46,3.42,5.53l9.34,4.61c.93.46,1.87.61,2.8.61s1.87-.15,2.8-.61l9.34-4.61c2.18-1.08,3.42-3.23,3.42-5.53Z"/>'
       '<path d="M46.32,51.22c0-.45-.31-.91-.79-1.21l-9.74-4.69-2.2,1.06v7.72l6.13,6.51c.31.45.94.61,1.57.45l6.13-1.36-1.1-8.48Z"/>'
       '<path d="M110.44,49.64c-.48.15-.79.62-.79,1.24l-1.11,8.96c2.06.31,4.12.77,6.03,1.24.63.15,1.27-.15,1.59-.62l4.76-6.18v-8.35l-1.43-.62-9.04,4.33Z"/>'
       '<path d="M121.47,57.98l-3.42,4.28c-1.09,1.38-2.95,2.14-4.66,1.68-24.41-5.5-48.51-5.5-71.68,0-.31.15-.78.15-1.09.15-1.24,0-2.49-.46-3.42-1.53l-4.66-5.04-1.24,1.22c-.62.61-.62,1.38-.16,1.99l4.04,4.89c.93,1.07,2.18,1.83,3.58,2.14,24.95-3.82,51.55-3.82,76.5,0,1.4-.31,2.64-1.07,3.58-2.14l4.04-4.89c.47-.61.47-1.53-.16-1.99l-1.24-.76Z"/>')
WORD = ('<path d="M28.27,84.08c0-7.47-6.42-11.75-14.13-11.75S0,76.61,0,84.08s6.42,11.79,14.13,11.79,14.13-4.29,14.13-11.79ZM22.7,84.08c0,4.32-3.06,7.04-8.56,7.04s-8.56-2.72-8.56-7.04,3.06-7.04,8.56-7.04,8.56,2.72,8.56,7.04Z"/>'
        '<path d="M52.47,77.3h-5.18l-6.51,12.67-6.71-12.67h-5.63l9.44,17.84h5.37l9.22-17.84Z"/>'
        '<path d="M73.88,86.66c0-4.81-3.91-9.76-10.68-9.76s-11.66,3.11-11.66,9.33,5.01,9.3,11.72,9.3c5.28,0,9.96-2.55,10.78-5.8h-5.67c-.65,1.38-2.34,2.1-5.21,2.1-3.22,0-5.99-1.41-6.64-4.32h17.36v-.85ZM56.66,84.31c.78-2.75,3.32-3.63,6.51-3.63,2.77,0,5.15,1.67,5.31,3.63h-11.82Z"/>'
        '<path d="M88.92,76.91c-3.81,0-6.32.65-7.55,3.54v-3.14h-4.98v17.84h5.31v-8.74c0-4.06,4.36-4.55,7.23-4.58v-4.91Z"/>'
        '<path d="M110,82.34c-.75-3.54-3.35-5.44-9.9-5.44-3.81,0-6.51.49-8.11,1.51-1.56,1.01-2.51,2.13-2.51,4.13,0,4.45,4.2,4.91,7.03,5.24,1.56.2,3.39.26,5.63.39,1.82.1,2.87.56,2.87,1.51,0,1.67-2.35,1.93-4.75,1.93-2.93,0-5.57-.49-5.93-2.19h-5.31c0,2.16,1.53,3.99,3.13,4.88,1.56.85,3.42,1.24,7.75,1.24,7.69,0,10.29-2.29,10.29-6.48,0-4.91-6.55-4.65-11.79-5.17-2.18-.23-3.61-.46-3.61-1.57,0-1.21,1.5-1.77,5.34-1.77,2.67,0,3.91.43,4.62,2l5.24-.2Z"/>'
        '<path d="M118.07,77.3h-5.28v17.84h5.28v-17.84ZM118.17,74.09c0-1.24-1.24-2.23-2.74-2.23s-2.7.98-2.7,2.23,1.21,2.23,2.7,2.23,2.74-1.01,2.74-2.23Z"/>'
        '<path d="M127.02,72.39l-5.08,1.7v3.21h-2.47v3.67h2.47v8.45c0,4.06,1.37,6.12,5.18,6.12,1.5,0,2.8-.62,3.16-1.21v-3.99c-.29.36-1.11.72-1.95.72-.91,0-1.3-.39-1.3-1.8v-8.28h3.16v-3.67h-3.16v-4.91Z"/>'
        '<path d="M153.84,86.66c0-4.81-3.91-9.76-10.68-9.76s-11.66,3.11-11.66,9.33,5.01,9.3,11.72,9.3c5.28,0,9.97-2.55,10.78-5.8h-5.67c-.65,1.38-2.35,2.1-5.21,2.1-3.22,0-5.99-1.41-6.64-4.32h17.36v-.85ZM136.61,84.31c.78-2.75,3.32-3.63,6.51-3.63,2.77,0,5.15,1.67,5.31,3.63h-11.82Z"/>')
# horizontal lockup: hard hat (gold) + wordmark (white), per guide
LOGO_H = ('<svg class="logo-h" viewBox="0 0 418 67" role="img" aria-label="Oversite">'
          f'<g fill="#E0A100" transform="translate(-26 0)">{HAT}</g>'
          f'<g fill="#FFFFFF" transform="translate(110 -134.2) scale(2)">{WORD}</g></svg>')
MARK = f'<svg viewBox="26 0 96 67" xmlns="http://www.w3.org/2000/svg"><g fill="#E0A100">{HAT}</g></svg>'


TALL_LOGOS = {"hdr", "lda", "hmb", "gha"}


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
        nxt = f'<div class="next"><span class="owner">{e(who)}</span><span>{e(what)}</span></div>'
    return f"""
<article class="card" data-status="{st}" id="{c["slug"]}">
  <div class="logo-tile{" tall" if c["logo"] in TALL_LOGOS else ""}"><img src="logos/{c["logo"]}.png" alt="{e(c["name"])} logo"></div>
  <div class="card-body">
    <div class="card-head"><h3>{e(c["name"])}</h3><span class="chip {st}">{STATUS_LABEL[st]}</span></div>
    <dl class="stats">
      <div><dt>Seats, Oversite / Stripe</dt><dd>{e(c["seats"])}{seats_note}</dd></div>
      <div><dt>Billing</dt><dd>{e(c["billing"])}</dd></div>
      <div><dt>Open balance</dt><dd class="num">{e(c["open"])}</dd></div>
      <div><dt>Past due</dt><dd><span class="num{past_cls}">{e(c["past"])}</span></dd></div>
    </dl>
    <p class="term">{e(c["term"])}</p>
    <ul class="notes">{notes}</ul>
    {subs}
    {nxt}
  </div>
</article>"""


def bars():
    mx = OPEN_BY[0][1]
    out = []
    for name, v in OPEN_BY:
        w = max(v / mx * 100, 1.2)
        pct = v / OPEN_TOTAL * 100
        out.append(f'<div class="bar-row"><span class="bar-label">{e(name)}</span>'
                   f'<span class="bar-track"><span class="bar-fill" style="width:{w:.1f}%"></span></span>'
                   f'<span class="bar-val"><b class="num">{money(v)}</b><em>{pct:.1f}%</em></span></div>')
    return "".join(out)


def tasks():
    rows = "".join(
        f'<tr><td><span class="owner">{o}</span></td><td>{e(t)}</td><td class="when">{e(d)}</td><td class="who">{e(k)}</td></tr>'
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
:root{--navy:#1A2040;--navy2:#232A52;--navy3:#2D356A;--ink:#0F1330;--ink2:#3A3F5A;--ink3:#6B6E82;--sky:#5DA9DE;--gold:#E0A100;--gold-l:#F0B830;--cream:#FDF8EA;--line:rgba(15,19,48,.12);--line-d:rgba(255,255,255,.12)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fff;color:var(--ink2);font:400 16px/1.65 'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:'Nunito',system-ui,sans-serif;font-weight:900;color:var(--ink);letter-spacing:-.01em;margin:0}
.mono,.eyebrow,dt,.chip,.owner,th,.bar-val em,.term,.foot-mono,.filters button{font-family:'JetBrains Mono',ui-monospace,monospace}
.wrap{max-width:1240px;margin:0 auto;padding:0 32px}
.eyebrow{font-size:12px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin:0 0 18px}
.eyebrow::before{content:"";display:inline-block;width:14px;height:2px;background:var(--gold);margin-right:10px;vertical-align:middle}
.lede{font-size:19px;line-height:1.6;margin:0}
.num{font-variant-numeric:tabular-nums}

/* top bar */
.top{position:sticky;top:0;z-index:20;background:rgba(26,32,64,.88);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line-d)}
.top .wrap{display:flex;align-items:center;gap:28px;height:68px}
.logo-h{height:30px;width:auto;display:block}
.top nav{margin-left:auto;display:flex;align-items:center;gap:26px;font-size:14px;font-weight:500}
.top nav a{color:#c9cde0;text-decoration:none}
.top nav a:hover{color:var(--gold-l)}
.top nav a.cta{background:var(--gold);color:var(--ink);font-weight:700;padding:8px 16px;border-radius:6px}
.top nav a.cta:hover{background:var(--gold-l);color:var(--ink)}

/* dark bands: tech grid + gold glow */
.dark{position:relative;overflow:hidden;background:var(--navy);color:#c9cde0}
.dark::before{content:"";position:absolute;inset:0;background-image:linear-gradient(var(--line-d) 1px,transparent 1px),linear-gradient(90deg,var(--line-d) 1px,transparent 1px);background-size:56px 56px;opacity:.55;-webkit-mask-image:radial-gradient(ellipse at 70% 20%,#000 0,transparent 70%);mask-image:radial-gradient(ellipse at 70% 20%,#000 0,transparent 70%);pointer-events:none}
.dark>.wrap{position:relative;z-index:1}
.dark h2,.dark h1,.dark h3{color:#fff}
.glow::after{content:"";position:absolute;width:640px;height:640px;right:-120px;top:-220px;background:radial-gradient(circle,rgba(224,161,0,.34) 0,rgba(224,161,0,0) 62%);filter:blur(30px);pointer-events:none}

.hero{padding:104px 0 88px}
.hero h1{font-size:clamp(40px,6.2vw,80px);line-height:1.04;max-width:860px;margin-bottom:24px}
.hero .lede{max-width:640px;color:#c9cde0}
.statblock{display:grid;grid-template-columns:repeat(4,1fr);margin-top:56px;background:var(--navy2);border:1px solid var(--line-d);border-radius:14px}
.stat{padding:28px 30px;min-width:0}
.stat+.stat{border-left:1px solid var(--line-d)}
.stat b{display:block;font:900 clamp(26px,3.2vw,40px)/1.1 'Nunito',sans-serif;color:var(--gold);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.stat span{display:block;margin-top:10px;font:500 11px 'JetBrains Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:#9aa0bd}
.stat small{display:block;margin-top:4px;font-size:14px;color:#c9cde0}

/* light bands */
.band{padding:96px 0}
.band.tight{padding:80px 0 24px}
h2.title{font-size:clamp(30px,4vw,48px);line-height:1.1;margin-bottom:14px}
.sub{max-width:640px;margin:0 0 40px;color:var(--ink3);font-size:17px}
.panel{background:#fff;border:1px solid var(--line);border-radius:14px;padding:32px}
.bar-row{display:grid;grid-template-columns:120px 1fr 210px;gap:18px;align-items:center;margin:14px 0}
.bar-label{font-weight:700;color:var(--ink);font-size:15px}
.bar-track{height:12px;background:#ECEEF6;border-radius:100px;overflow:hidden}
.bar-fill{display:block;height:100%;background:var(--sky);border-radius:100px}
.bar-val{text-align:right;white-space:nowrap}
.bar-val b{font:800 17px 'Nunito',sans-serif;color:var(--ink)}
.bar-val em{font-style:normal;font-size:12px;color:var(--ink3);margin-left:10px}
.fine{margin:20px 0 0;font-size:14px;color:var(--ink3)}

.filters{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 32px}
.filters button{background:#fff;color:var(--ink);border:1px solid var(--ink);border-radius:8px;padding:9px 16px;font-size:12px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;cursor:pointer;transition:background .15s,border-color .15s}
.filters button:hover{border-color:var(--gold);background:var(--cream)}
.filters button[aria-pressed=true]{background:var(--gold);border-color:var(--gold);font-weight:700}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}
.card{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;scroll-margin-top:92px;transition:border-color .2s,transform .2s,box-shadow .2s}
.card:hover{border-color:var(--gold);transform:translateY(-3px);box-shadow:0 14px 34px -18px rgba(26,32,64,.35)}
.card[hidden]{display:none}
.logo-tile{height:104px;display:flex;align-items:center;padding:0 32px;background:var(--navy);position:relative}
.logo-tile img{height:36px;width:auto;max-width:76%;object-fit:contain;display:block}
.logo-tile.tall img{height:54px}
.card-body{padding:26px 32px 30px;display:flex;flex-direction:column;gap:14px;flex:1}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:14px}
.card-head h3{font-size:24px;line-height:1.2}
.chip{display:inline-flex;align-items:center;gap:8px;white-space:nowrap;font-size:10.5px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;padding:6px 12px;border:1px solid var(--line);border-radius:100px;color:var(--ink2);background:#fff}
.chip::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--sky)}
.chip.attention{background:var(--cream);border-color:rgba(224,161,0,.55);color:var(--ink)}
.chip.attention::before{background:var(--gold)}
.chip.hold{color:var(--ink3)}
.chip.hold::before{background:transparent;border:1.5px solid var(--ink3)}
.stats{display:grid;grid-template-columns:1fr 1fr;gap:16px 20px;margin:2px 0 0}
.stats div{min-width:0}
.stats dt{font-size:10.5px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3)}
.stats dd{margin:4px 0 0;font:800 18px/1.3 'Nunito',sans-serif;color:var(--ink)}
.muted{color:var(--ink3);font:400 14px 'DM Sans',sans-serif}
.warn{display:inline-block;background:var(--cream);box-shadow:inset 3px 0 0 var(--gold);padding:0 10px;border-radius:6px}
.term{margin:0;font-size:12px;letter-spacing:.04em;color:var(--ink3)}
.notes{margin:0;padding-left:18px;font-size:15px;line-height:1.6}
.notes li{margin:6px 0}
.notes li::marker{color:var(--gold)}
.next{display:flex;gap:12px;align-items:flex-start;margin-top:auto;padding:14px 16px;background:var(--cream);border-left:3px solid var(--gold);border-radius:0 8px 8px 0;font-size:15px;color:var(--ink)}
.owner{display:inline-block;font-size:10.5px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;padding:3px 9px;border-radius:6px;background:var(--ink);color:#fff;white-space:nowrap;line-height:1.6}
table{width:100%;border-collapse:collapse}
.subs{font-size:14px;margin-top:2px}
.subs th,.subs td{padding:8px 8px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.subs thead th{font-size:10.5px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3)}
.subs th[scope=row]{font:800 15px 'Nunito',sans-serif;color:var(--ink)}
.subs .num{text-align:right;font-weight:700;color:var(--ink)}
.subs .subnote td{color:var(--ink2);font-size:14px;line-height:1.55;padding-top:0;padding-bottom:12px}

/* action list (dark band) */
.tasks{font-size:15.5px}
.tasks th{font-size:10.5px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:#9aa0bd;text-align:left;padding:10px 14px;border-bottom:1px solid var(--line-d)}
.tasks td{padding:16px 14px;border-bottom:1px solid var(--line-d);vertical-align:top;color:#dfe2f0}
.tasks .owner{background:rgba(255,255,255,.1);border:1px solid var(--line-d)}
.tasks .when{white-space:nowrap;color:#fff;font-weight:700}
.tasks .who{color:#9aa0bd;font-size:14px}
.tasks-wrap{background:var(--navy2);border:1px solid var(--line-d);border-radius:14px;padding:14px 18px}

/* forms */
.qgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}
.qcard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:32px;scroll-margin-top:92px;transition:border-color .2s}
.qcard:hover{border-color:var(--gold)}
.qcard h3{font-size:24px;margin-bottom:6px}
.qcard .intro{margin:0 0 22px;font-size:15px;color:var(--ink3)}
.q{border:0;margin:0 0 20px;padding:0;min-width:0}
.q legend{padding:0;margin-bottom:8px;font:700 15px 'DM Sans',sans-serif;color:var(--ink)}
.opt{display:flex;gap:12px;align-items:flex-start;padding:11px 14px;border:1px solid var(--line);border-radius:8px;margin:8px 0;cursor:pointer;font-size:15px;line-height:1.45;transition:border-color .15s,background .15s}
.opt:hover{border-color:var(--gold)}
.opt:has(input:checked){border-color:var(--gold);background:var(--cream)}
.opt input{margin-top:4px;accent-color:var(--gold)}
.fl{display:block;font:500 11px 'JetBrains Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3)}
.fl input,.fl textarea{display:block;width:100%;margin-top:8px;background:#fff;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:11px 14px;font:400 16px 'DM Sans',sans-serif;letter-spacing:0;text-transform:none}
.fl input:focus,.fl textarea:focus,.opt:focus-within{outline:2px solid var(--gold);outline-offset:1px;border-color:var(--gold)}
.qform>.fl,.q .fl{margin-bottom:4px}
.row{margin:18px 0 20px}
button[type=submit]{background:var(--gold);color:var(--ink);border:0;border-radius:8px;padding:13px 22px;font:800 15px 'Nunito',sans-serif;cursor:pointer;transition:background .15s}
button[type=submit]:hover{background:var(--gold-l)}
button[type=submit]:disabled{opacity:.6;cursor:wait}
.status{margin:14px 0 0;font-size:14px;font-weight:700;min-height:1.3em}
.status.ok{color:var(--ink)}
.status.ok::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--sky);margin-right:8px}
.status.err{color:var(--ink);background:var(--cream);border-left:3px solid var(--gold);padding:8px 12px;border-radius:0 8px 8px 0}
.hp{position:absolute;left:-9999px;height:0;overflow:hidden}

footer{background:var(--ink);color:#9aa0bd;padding:56px 0 40px}
footer .logo-h{height:34px;margin-bottom:28px}
footer .rule{border-top:1px solid var(--line-d);padding-top:22px;display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
.foot-mono{font-size:11px;letter-spacing:.14em;text-transform:uppercase}
footer p{margin:0 0 6px;font-size:14px;max-width:720px}

@media(max-width:900px){.statblock{grid-template-columns:repeat(2,1fr)}.stat:nth-child(3){border-left:0}.stat:nth-child(n+3){border-top:1px solid var(--line-d)}.grid,.qgrid{grid-template-columns:1fr}.top nav a:not(.cta){display:none}.bar-row{grid-template-columns:96px 1fr}.bar-val{grid-column:1/-1;text-align:left;margin-top:-6px}}
@media(max-width:600px){.wrap{padding:0 20px}.hero{padding:64px 0 56px}.band{padding:64px 0}.band.tight{padding:56px 0 16px}.panel,.qcard{padding:22px}.card-body{padding:22px}.stat{padding:20px}.logo-h{height:26px}.tasks thead{display:none}.tasks tr{display:block;padding:12px 0;border-bottom:1px solid var(--line-d)}.tasks td{display:block;border:0;padding:3px 0}.tasks .when{white-space:normal}.tasks-wrap{padding:8px 16px}.card-head{flex-direction:column;gap:10px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.card,.qcard{transition:none}.card:hover{transform:none}}
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
    from urllib.parse import quote
    cards = "".join(card(c) for c in CUSTOMERS)
    fav = "data:image/svg+xml," + quote(MARK, safe="/:=,;()'")
    qforms = "".join(FORMS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1A2040">
<title>Oversite AR Review</title>
<link rel="icon" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800;900&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">{LOGO_H}
<nav><a href="#customers">Customers</a><a href="#actions">Action list</a><a href="#questions" class="cta">Answer questions</a></nav></div></header>
<main>
<section class="dark glow hero"><div class="wrap">
<p class="eyebrow">Accounts receivable &middot; {AS_OF}</p>
<h1>14 customers. One clear picture.</h1>
<p class="lede">Where every customer under contract stands, built from Stripe, the Oversite database, and the PNFP bank deposits. The questions that need your call are at the bottom.</p>
<div class="statblock">
<div class="stat"><b>{money(OPEN_TOTAL)}</b><span>Open balance</span><small>Stripe, after clean-up</small></div>
<div class="stat"><b>{money(PAST_TOTAL)}</b><span>Past due</span><small>Volkert and Chen Moore</small></div>
<div class="stat"><b>{money(OPEN_TOTAL - PAST_TOTAL)}</b><span>Not yet due</span><small>Mostly Collier, due 10/29</small></div>
<div class="stat"><b>{len(CUSTOMERS)}</b><span>Customers</span><small>{n_good} good, {n_att} attention, {n_hold} on hold</small></div>
</div>
</div></section>

<section class="band tight"><div class="wrap">
<p class="eyebrow">Concentration</p>
<h2 class="title">Where the open balance sits</h2>
<p class="sub">Collier alone is most of it. Everything else is small, but Volkert Virginia Beach is the oldest.</p>
<div class="panel">{bars()}
<p class="fine">Excludes HMB TUN2DAXI-0004 ($329.25), which is likely stale and unverified, and unbilled catch-ups.</p></div>
</div></section>

<section class="band" id="customers"><div class="wrap">
<p class="eyebrow">01 &middot; Customers</p>
<h2 class="title">Every account, top down</h2>
<p class="sub">Seats are active users in Oversite, then seats billed in Stripe. Viewers are not counted.</p>
<div class="filters" role="group" aria-label="Filter customers">
<button type="button" data-f="all" aria-pressed="true">All {len(CUSTOMERS)}</button>
<button type="button" data-f="attention" aria-pressed="false">Needs attention {n_att}</button>
<button type="button" data-f="hold" aria-pressed="false">On hold {n_hold}</button>
<button type="button" data-f="good" aria-pressed="false">Good standing {n_good}</button>
</div>
<div class="grid">{cards}</div>
</div></section>

<section class="dark band" id="actions"><div class="wrap">
<p class="eyebrow">02 &middot; Action list</p>
<h2 class="title">What happens next, in priority order</h2>
<p class="sub" style="color:#c9cde0">Owner, timing, and whether Cowork can do the first draft.</p>
<div class="tasks-wrap">{tasks()}</div>
</div></section>

<section class="band" id="questions"><div class="wrap">
<p class="eyebrow">03 &middot; Questions for Marissa</p>
<h2 class="title">Your call, in a few clicks</h2>
<p class="sub">Quick answers are fine. Each form goes straight to Matt.</p>
<div class="qgrid">{qforms}</div>
</div></section>
</main>
<footer><div class="wrap">{LOGO_H}
<div class="rule"><div><p>Golden Spike Technologies, Inc. (Oversite). Internal, not for distribution.</p>
<p>Sources: Stripe, Oversite production database, PNFP deposits through 10/27/2026. Counts and balances are a snapshot and will drift.</p></div>
<span class="foot-mono">AI is the next evolution of UI/UX</span></div></div></footer>
<script>{JS}</script>
</body>
</html>
'''


if __name__ == "__main__":
    open("index.html", "w").write(page())
    print("wrote index.html")
