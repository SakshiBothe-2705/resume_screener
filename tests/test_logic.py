import os
import sys

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.processor import rank_resumes

def test_ranking():
    print("Testing Ranking Logic...")
    
    # Create dummy files
    os.makedirs('test_uploads', exist_ok=True)
    
    resume1 = "test_uploads/python_expert.txt"
    resume2 = "test_uploads/chef.txt"
    
    with open(resume1, 'w') as f:
        f.write("I am an expert in Python, Flask, and Machine Learning. I love coding.")
        
    with open(resume2, 'w') as f:
        f.write("I am an expert in cooking, baking, and grilling. I love food.")
        
    job_desc = "Looking for a Python Developer with Flask and ML experience."
    
    results = rank_resumes(job_desc, [resume1, resume2])
    
    print("\nResults:")
    for r in results:
        print(f"{r['filename']}: {r['score']}%")
        
    # Verification
    if results[0]['filename'] == 'python_expert.txt' and results[0]['score'] > results[1]['score']:
        print("\nSUCCESS: Python expert ranked higher.")
    else:
        print("\nFAILURE: Ranking logic is incorrect.")
        
    # Cleanup
    try:
        os.remove(resume1)
        os.remove(resume2)
        os.rmdir('test_uploads')
    except:
        pass

if __name__ == "__main__":
    test_ranking()
