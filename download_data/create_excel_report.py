import sqlite3
import pandas as pd

def create_excel_report(db_path, output_file):
    conn = sqlite3.connect(db_path)

    # Query the CadetAchv table
    query = """
        SELECT CAPID, CadetAchvID, PhyFitTest, LeadLabDateP, LeadLabScore, AEDateP, AEScore, AEMod, AETest, MoralLDateP, ActivePart, OtherReq, SDAReport, UsrID, DateMod, FirstUsr, DateCreated, DrillDate, DrillScore, LeadCurr, CadetOath, AEBookValue, MileRun, ShuttleRun, SitAndReach, PushUps, CurlUps, HFZID, StaffServiceDate, TechnicalWritingAssignment, TechnicalWritingAssignmentDate, OralPresentationDate, SpeechDate, LeadershipEssayDate 
        FROM CadetAchv;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Excel report generated: {output_file}")

if __name__ == "__main__":
    create_excel_report("capwatch.db", "cadet_achievements_report.xlsx")
