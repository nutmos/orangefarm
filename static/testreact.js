var TestReact = React.createClass({
    render: function() {
        return <p>This is the test react class.</p>;
    }
});

ReactDOM.render(
    <TestReact />,
    document.getElementById('content')
);
