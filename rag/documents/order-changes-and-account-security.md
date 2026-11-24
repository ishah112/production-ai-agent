---
document_id: order-changes-account-security
title: Order Changes, Cancellations, and Account Security
version: 1.0
effective_date: 2026-01-01
audience: customer-support-agent
---

# Order Changes, Cancellations, and Account Security

## 1. Purpose and scope

This policy explains when a customer may change or cancel a direct Northstar
Supply order and how support should protect account and order information. It
applies to domestic physical-goods orders. It does not authorize a support
agent or an AI system to bypass account verification, payment controls, or the
order's recorded state.

## 2. Order state determines available actions

An order moves through operational states such as **received**, **processing**,
**packed**, **shipped**, **delivered**, and **cancelled**. Exact state names may
differ in the order system. Check the live order record before telling a
customer that a change or cancellation is available.

### 2.1 Before packing

While an order is received or processing and has not been packed, support may
request an item, quantity, or address correction. Changes are subject to
inventory and payment reauthorization. Tell the customer the change is
complete only after the system confirms it.

### 2.2 After packing or shipment

Once packed, edits are not guaranteed. After carrier handoff, use the shipping
and delivery process for an intercept or address correction. A cancellation
request does not stop a parcel already in carrier possession; if delivery
occurs, the customer may request a return under the returns policy.

## 3. Cancellation and payment authorization

If cancellation is accepted before fulfillment, the order is marked cancelled
and any captured payment is refunded according to the refund policy. A payment
authorization hold may disappear on a different schedule from a completed
refund; do not describe an authorization release as a refund unless the payment
record identifies it as one.

If fulfillment has started, submit a cancellation request for review. Do not
promise success until the order system confirms cancellation. If cancellation
fails because shipment has begun, explain the return option after delivery.

## 4. Split, bundled, and promotional orders

An order can contain multiple items with separate fulfillment states. A
cancellation of one line does not imply cancellation of the whole order.
Review the affected line and any associated discount before confirming the
result.

Removing an item from a bundle may change the discount applied to the items
the customer keeps. The order system's recalculated total is authoritative;
support must not promise that the original bundle price remains unchanged.
Promotional codes may be single-use and may not be restored after cancellation
unless the promotion's terms explicitly allow it.

## 5. Identity verification and permitted disclosure

Use the approved account verification flow before changing an order or
disclosing non-public order details. A matching order number by itself is not
sufficient authentication for a high-impact action such as changing the
delivery address or cancelling an order.

Support may ask for the order number and a limited verification factor allowed
by the workflow. Never request or repeat a password, one-time sign-in code,
full card number, card security code, or full government identifier. If a
customer volunteers such data in chat, do not echo it; direct them to the
secure channel and follow the incident procedure where required.

## 6. Requests from a third party

Do not change or disclose an order at the request of a person who has not
passed the account's authorized verification process, even if that person
claims to be a family member, coworker, or recipient. A recipient may be able
to discuss delivery logistics through the carrier, but merchant account data
and payment details remain private.

## 7. Suspected unauthorized activity

If a customer reports an order they do not recognize, do not cancel, refund,
or change it solely on an unverified chat claim. Secure the account through
the established account-security workflow and route the order for fraud
review. Do not reveal the suspected attacker's contact or payment details.

If support sees an address change or cancellation inconsistent with the
verified account history, preserve the event record and escalate. Do not
overwrite or delete audit information to make the order appear normal.

## 8. Data minimization in agent responses

Answer only the question asked and disclose only the minimum order information
needed. For example, an order-status response may identify the purchased item
and current status after verification; it should not expose another customer's
email, full shipping address, payment instrument, or internal fraud notes.

The assistant must rely on authorized tools for customer-specific facts. A
policy document cannot confirm that a particular order was cancelled, changed,
or refunded. If a tool does not return the relevant field, say what information
is missing and route the request for lookup; do not infer the outcome.

## 9. Escalation criteria

Escalate requests involving suspected account takeover, conflicting order
ownership, an unauthorized address change, payment disputes, legal demands,
or requests to disclose another person's information. Do not make exceptions
to verification because a request is urgent or emotionally compelling.

## 10. Examples

- **Customer asks to change an address; order is processing:** Check whether
  packing has begun, complete verification, submit the change, and report
  success only when confirmed.
- **Customer asks to cancel; order is shipped:** Explain that cancellation
  cannot be guaranteed after carrier handoff and provide the return process.
- **A caller knows the order number but is not the verified account holder:**
  Do not disclose item, address, or payment details; use the verification
  workflow.
- **Order is cancelled but a card still shows a pending hold:** Check the
  payment record and distinguish an authorization hold from a submitted
  refund.

## 11. Policy precedence

Account-security controls and applicable law take precedence over convenience
or a general customer-service exception. For a specific order, use the live
order state and recorded support decisions. Never treat a policy example as
proof that an action occurred.
