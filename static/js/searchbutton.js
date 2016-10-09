var query = '';
var SearchBox = React.createClass ({
    getInitialState: function() {
        return {query: ''};
    },
    queryChange: function(evt) {
        this.setState({query: evt.target.value});
        query = evt.target.value;
        //console.log(query);
    },
    handleKeyPress: function(e) {
        if (e.charCode == 13) {
            console.log('enter press');
            window.location = query;
        }
    },
    render: function() {
        return <input onKeyPress={this.handleKeyPress} type="text" value={this.state.query} onChange={this.queryChange} placeholder="Search Site" />;
    }
});

var SearchButton = React.createClass({
    getInitialState: function() {
        return {};
    },
    handleSearch: function(e) {
        if (/\S/.test(query)) {
            window.location = query;
        }
    },
    render: function() {
        return (<div>
            <SearchBox />
            <button onClick={this.handleSearch} className="large success hollow button">Search</button>
            </div>);
    }
});

ReactDOM.render(
    React.createElement(SearchButton, {}),
    document.getElementById('search-button')
);

