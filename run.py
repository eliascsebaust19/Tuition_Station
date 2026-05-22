from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print("  TuitionStation - Educational Marketplace")
    print("  Running on http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)
