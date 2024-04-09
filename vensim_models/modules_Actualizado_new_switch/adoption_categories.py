"""
Module adoption_categories
Translated using PySD version 3.13.4
"""


@component.add(name="early adopters", comp_type="Constant", comp_subtype="Normal")
def early_adopters():
    return 0.135


@component.add(name="early majority", comp_type="Constant", comp_subtype="Normal")
def early_majority():
    return 0.34


@component.add(name="innovators", comp_type="Constant", comp_subtype="Normal")
def innovators():
    return 0.025


@component.add(name="laggards", comp_type="Constant", comp_subtype="Normal")
def laggards():
    return 0.16


@component.add(name="late majority", comp_type="Constant", comp_subtype="Normal")
def late_majority():
    return 0.34
