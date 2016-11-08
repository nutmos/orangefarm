var CitySelect = React.createClass({
    parseJSON: function() {
        return JSON.parse('/city/get-city-by-country?country_id=');
    },
    render: function() {
        var data = this.parseJSON();
        return (
            <select id="city-list" name="city-list">
                <option value="">Select City</option>
            </select>
        );
    }
});

ReactDOM.render(
    React.createElement(CitySelect, {}),
    document.getElementById('city-select')
);
