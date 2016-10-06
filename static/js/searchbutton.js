var SearchButton = React.createClass({
    getInitialState: function() {
        return {query: ''};
    },
    queryChange: function(evt) {
        this.setState({query: evt.target.value});
    },
    _buildLink: function() {
        console.log(this.state.query);
        return this.state.query;
    },
    render: function() {
        return (<div>
            <input type="text" value={this.state.query} onChange={this.queryChange} placeholder="Search Site" />
            <a href={this._buildLink()} className="success hollow button" >Search</a>;
            </div>
        );
    }
});
ReactDOM.render(
    React.createElement(SearchButton, {query: ''}),
    document.getElementById('search-button')
);

