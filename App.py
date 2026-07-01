from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Comment, SentimentAnalysis
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly
import plotly.graph_objs as go
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiment_analysis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize VADER analyzer
vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_textblob(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        label = 'Positive'
    elif polarity < -0.1:
        label = 'Negative'
    else:
        label = 'Neutral'
    
    confidence = abs(polarity)
    return polarity, label, confidence

# At the top of app.py, after imports
vader_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER"""
    scores = vader_analyzer.polarity_scores(text)  # Use global analyzer
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = 'Positive'
    elif compound <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'
    
    confidence = abs(compound)
    
    return {
        'sentiment': sentiment,
        'score': compound,
        'confidence': confidence
    }

def generate_wordcloud(comments_list, sentiment_filter=None):
    """
    Generate word cloud from comments
    
    Args:
        comments_list: List of comment dictionaries with 'text' and 'sentiment'
        sentiment_filter: 'Positive', 'Negative', 'Neutral', or None for all
    
    Returns:
        Base64 encoded image string for HTML display
    """
    
    # Filter comments by sentiment if specified
    if sentiment_filter:
        filtered_comments = [
            comment['text'] for comment in comments_list 
            if comment['sentiment'] == sentiment_filter
        ]
    else:
        filtered_comments = [comment['text'] for comment in comments_list]
    
    # Combine all text into one string
    text = ' '.join(filtered_comments)
    
    # If no text, return None
    if not text.strip():
        return None
    
    # Create custom stopwords (add domain-specific words to ignore)
    custom_stopwords = set(STOPWORDS)
    custom_stopwords.update([
        'policy', 'government', 'people', 'think', 'good', 'bad',
        'really', 'would', 'could', 'should', 'much', 'many',
        'one', 'two', 'also', 'well', 'way', 'time', 'need'
    ])
    
    # Configure word cloud
    wordcloud = WordCloud(
        width=800,                    # Image width
        height=400,                   # Image height
        background_color='white',     # Background color
        max_words=100,               # Maximum words to show
        stopwords=custom_stopwords,  # Words to ignore
        colormap='viridis',          # Color scheme
        collocations=False,          # Don't group word pairs
        relative_scaling=0.5,        # Size difference between words
        min_font_size=10             # Minimum font size
    ).generate(text)
    
    # Create matplotlib figure
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Remove axes
    
    # Save to memory buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
    img_buffer.seek(0)
    plt.close()  # Close figure to free memory
    
    # Convert to base64 for HTML embedding
    img_base64 = base64.b64encode(img_buffer.read()).decode()
    
    return f"data:image/png;base64,{img_base64}"


# Your existing route functions start after this
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process and analyze comments"""
    comments_text = request.form.get('comments')
    method = request.form.get('method', 'textblob')
    session_name = request.form.get('session_name', f'Analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
    
    if not comments_text:
        flash('Please enter comments to analyze', 'error')
        return redirect(url_for('index'))
    
    # Split comments by newlines
    comment_lines = [line.strip() for line in comments_text.split('\n') if line.strip()]
    
    if not comment_lines:
        flash('No valid comments found', 'error')
        return redirect(url_for('index'))
    
    results = []
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
    total_sentiment = 0
    
    for comment_text in comment_lines:
        if method == 'vader':
            score, label, confidence = analyze_sentiment_vader(comment_text)
        else:
            score, label, confidence = analyze_sentiment_textblob(comment_text)
        
        # Save to database
        comment = Comment(
            text=comment_text,
            sentiment_score=score,
            sentiment_label=label,
            confidence=confidence,
            method=method.upper()
        )
        db.session.add(comment)
        
        results.append({
            'text': comment_text,
            'sentiment': label,
            'score': round(score, 3),
            'confidence': round(confidence, 3)
        })
        
        sentiment_counts[label] += 1
        total_sentiment += score
    
    # Calculate overall statistics
    total_comments = len(comment_lines)
    avg_sentiment = total_sentiment / total_comments if total_comments > 0 else 0
    
    # Save analysis session
    analysis = SentimentAnalysis(
        session_name=session_name,
        total_comments=total_comments,
        positive_count=sentiment_counts['Positive'],
        negative_count=sentiment_counts['Negative'],
        neutral_count=sentiment_counts['Neutral'],
        avg_sentiment=avg_sentiment
    )
    db.session.add(analysis)
    db.session.commit()
    
    # Create visualization
    chart_data = create_sentiment_chart(sentiment_counts)
        # Generate word clouds (add this section)
    try:
        # Overall word cloud (all comments)
        overall_wordcloud = generate_wordcloud(results)
        
        # Sentiment-specific word clouds (only if comments exist)
        positive_wordcloud = generate_wordcloud(results, 'Positive') if sentiment_counts['Positive'] > 0 else None
        negative_wordcloud = generate_wordcloud(results, 'Negative') if sentiment_counts['Negative'] > 0 else None
        neutral_wordcloud = generate_wordcloud(results, 'Neutral') if sentiment_counts['Neutral'] > 0 else None
        
    except Exception as e:
        print(f"Word cloud generation error: {e}")
        overall_wordcloud = None
        positive_wordcloud = None
        negative_wordcloud = None
        neutral_wordcloud = None

    return render_template('results.html', 
                         results=results, 
                         sentiment_counts=sentiment_counts,
                         avg_sentiment=round(avg_sentiment, 3),
                         total_comments=total_comments,
                         session_name=session_name,
                         chart_data=chart_data,
                         method=method.upper(),
                         overall_wordcloud=overall_wordcloud,
                         positive_wordcloud=positive_wordcloud,
                         negative_wordcloud=negative_wordcloud,
                         neutral_wordcloud=neutral_wordcloud)


def create_sentiment_chart(sentiment_counts):
    """Create a pie chart for sentiment distribution"""
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())
    colors = ['#28a745', '#dc3545', '#ffc107']  # Green, Red, Yellow
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        hole=0.3
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        font=dict(size=16),
        showlegend=True
    )
    
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return chart_json

@app.route('/history')
def history():
    """Show analysis history"""
    analyses = SentimentAnalysis.query.order_by(SentimentAnalysis.analysis_date.desc()).all()
    return render_template('history.html', analyses=analyses)

@app.route('/api/comments')
def api_comments():
    """API endpoint to get recent comments"""
    comments = Comment.query.order_by(Comment.timestamp.desc()).limit(100).all()
    return jsonify([{
        'id': c.id,
        'text': c.text,
        'sentiment': c.sentiment_label,
        'score': c.sentiment_score,
        'confidence': c.confidence,
        'method': c.method,
        'timestamp': c.timestamp.isoformat()
    } for c in comments])

@app.route('/export/<int:analysis_id>')
def export_analysis(analysis_id):
    """Export analysis results as CSV"""
    analysis = SentimentAnalysis.query.get_or_404(analysis_id)
    comments = Comment.query.filter(
        Comment.timestamp >= analysis.analysis_date
    ).order_by(Comment.timestamp.desc()).all()
    
    # Create DataFrame
    data = [{
        'Comment': c.text,
        'Sentiment': c.sentiment_label,
        'Score': c.sentiment_score,
        'Confidence': c.confidence,
        'Method': c.method,
        'Timestamp': c.timestamp
    } for c in comments]
    
    df = pd.DataFrame(data)
    
    # Return as CSV download
    from flask import make_response
    output = df.to_csv(index=False)
    response = make_response(output)
    response.headers["Content-Disposition"] = f"attachment; filename=sentiment_analysis_{analysis_id}.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
