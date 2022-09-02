Placeholder description: (The WIP continues)

The problem:

Bid adjustments in Google Adwords are multiplicative.
Assume a base bid of 1€. We set a bid adjustment of 150% for mobile users because they increase the value of these particular bids click by 0.50€. And another bid adjustment for bids that happen mondays by 120% (0.20€ value increase). The click is worth 1.70€ to us but the final bid will be 1€ ∗ 1.5 ∗ 1.2 = 1.80€. With large bid adjustments across multiple bid adjustment groups and dimensions this leads to overspend.

Definitions:
Group:
Dimension: 

Caviats:

Assums other aspects of the campaign are already optimized an correct and thus increasing the amount of clicks will increase converions.

The two metrics that come to mind for this algorithm are CPA and ROAS, since ROAS is more vulnerable to outliers than CPA, and since 0 Conversions would make use unable to calculate a CPA we will use the inverse of CPA, ICPA as coremetric for the calculations.

Total ICPA Method


(how we find the error value)
(how xiter finds the best startingvalues for the opt.min() )
(example with the spreadsheet)
(stuff)
(simping for the author)
