var Button1 = React.createClass({
    getHref: function() {
        return "http://www.facebook.com";
    },
    render: function() {
        return <a href={this.getHref()} className="button">Button 1</a>;
    }
});
var app = React.createElement(Button1, {});

ReactDOM.render(
    app,
    document.getElementById('button1')
);

