var query = '';
var SearchButton = React.createClass({
    getInitialState: function() {
        return {query: ''};
    },
    handleSearch: function(e) {
        if (/\S/.test(query)) {
            window.location = query;
        }
    },
    queryChange: function(e) {
        this.setState({query: e.target.value});
        query = e.target.value;
    },
    handleKeyPress: function(e) {
        if (e.charCode == 13) {
            if (/\S/.test(query)) {
                window.location = query;
            }
        }
    },
    render: function() {
        return (<div className="text-centered">
            <input onKeyPress={this.handleKeyPress} type="text" value={this.state.query} onChange={this.queryChange} placeholder="Search Site" />
            <button onClick={this.handleSearch} className="large success hollow button">Search</button>
            </div>);
    }
});

ReactDOM.render(
    React.createElement(SearchButton, {}),
    document.getElementById('search-button')
);

