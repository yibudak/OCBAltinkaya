odoo.define('web.TimeRangeMenuOptions', function (require) {
"use strict";

var core = require('web.core');
var _lt = core._lt;
var _t = core._t;

var PeriodOptions = [
    {description: _t('Last 7 Days'), optionId: 'last_7_days', groupId: 1},
    {description: _t('Last 30 Days'), optionId: 'last_30_days', groupId: 1},
    {description: _t('Last 365 Days'), optionId: 'last_365_days', groupId: 1},
    {description: _t('Today'), optionId: 'today', groupId: 2},
    {description: _t('This Week'), optionId: 'this_week', groupId: 2},
    {description: _t('This Month'), optionId: 'this_month', groupId: 2},
    {description: _t('This Quarter'), optionId: 'this_quarter', groupId: 2},
    {description: _t('This Year'), optionId: 'this_year', groupId: 2},
    {description: _t('Yesterday'), optionId: 'yesterday', groupId: 3},
    {description: _t('Last Week'), optionId: 'last_week', groupId: 3},
    {description: _t('Last Month'), optionId: 'last_month', groupId: 3},
    {description: _t('Last Quarter'), optionId: 'last_quarter', groupId: 3},
    {description: _t('Last Year'), optionId: 'last_year', groupId: 3},
];

var ComparisonOptions =  [
    {description: _t('Previous Period'), optionId: 'previous_period'},
    {description: _t('Previous Year'), optionId: 'previous_year'}
];

return {
    PeriodOptions: PeriodOptions,
    ComparisonOptions: ComparisonOptions,
};

});
