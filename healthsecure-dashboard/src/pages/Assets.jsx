import { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";

function Assets() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [critFilter, setCritFilter] = useState("All");
  const [statusFilter, setStatusFilter] = useState("All");
  const [showModal, setShowModal] = useState(false);
  const [newAsset, setNewAsset] = useState({
    name: "",
    type: "",
    criticality: "Medium",
    status: "Online",
    ip: "",
    owner: "",
  });
  const { token, isAdmin } = useAuth();

  useEffect(() => {
    fetch("http://localhost:8001/assets/", {
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setAssets(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching assets:", err);
        setLoading(false);
      });
  }, [token]);

  const totalAssets = assets.length;
  const onlineAssets = assets.filter((a) => a.status === "Online").length;
  const criticalAssets = assets.filter((a) => a.criticality === "Critical").length;
  const compromisedAssets = assets.filter((a) => a.status === "Compromised").length;

  const filteredAssets = useMemo(() => {
    return assets.filter((a) => {
      const q = search.toLowerCase();
      const matchesSearch =
        !q ||
        (a.name || "").toLowerCase().includes(q) ||
        (a.type || "").toLowerCase().includes(q) ||
        (a.ip || "").toLowerCase().includes(q);

      const matchesCrit = critFilter === "All" || a.criticality === critFilter;
      const matchesStatus = statusFilter === "All" || a.status === statusFilter;

      return matchesSearch && matchesCrit && matchesStatus;
    });
  }, [assets, search, critFilter, statusFilter]);

  if (loading) return <p style={{ padding: 20 }}>Loading assets...</p>;

  // ---- Simple inline styles to mimic dashboard look ----
  const page = { padding: 20, fontFamily: "system-ui, Arial, sans-serif" };
  const title = { fontSize: 28, fontWeight: 700, marginBottom: 4 };
  const subtitle = { color: "#6b7280", marginBottom: 20 };

  const cards = {
    display: "grid",
    gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
    gap: 16,
    marginBottom: 20,
  };

  const card = {
    background: "#fff",
    borderRadius: 12,
    padding: 16,
    boxShadow: "0 1px 6px rgba(0,0,0,0.08)",
    border: "1px solid #e5e7eb",
  };

  const cardLabel = { color: "#6b7280", fontSize: 13 };
  const cardValue = { fontSize: 28, fontWeight: 700 };

  const toolbar = {
    background: "#fff",
    borderRadius: 12,
    padding: 12,
    boxShadow: "0 1px 6px rgba(0,0,0,0.08)",
    border: "1px solid #e5e7eb",
    display: "flex",
    gap: 12,
    alignItems: "center",
    marginBottom: 12,
  };

  const input = {
    flex: 1,
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
    outline: "none",
  };

  const select = {
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
    background: "#fff",
  };

  const tableWrap = {
    background: "#fff",
    borderRadius: 12,
    boxShadow: "0 1px 6px rgba(0,0,0,0.08)",
    border: "1px solid #e5e7eb",
    overflow: "hidden",
  };

  const th = {
    textAlign: "left",
    padding: "12px 10px",
    fontSize: 12,
    color: "#6b7280",
    borderBottom: "1px solid #e5e7eb",
    background: "#f9fafb",
  };

  const td = {
    padding: "12px 10px",
    borderBottom: "1px solid #f1f5f9",
  };

  const buttonStyle = {
    background: "#2563eb",
    color: "#fff",
    border: "none",
    padding: "10px 16px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 500,
    fontSize: 14,
  };

  const modalOverlay = {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0,0,0,0.5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 1000,
  };

  const modalContent = {
    background: "#fff",
    borderRadius: 12,
    padding: 24,
    width: 400,
    maxWidth: "90%",
    boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
  };

  const modalTitle = {
    fontSize: 20,
    fontWeight: 600,
    marginBottom: 20,
  };

  const formGroup = {
    marginBottom: 16,
  };

  const label = {
    display: "block",
    fontSize: 14,
    fontWeight: 500,
    marginBottom: 6,
    color: "#374151",
  };

  const formInput = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
    outline: "none",
    fontSize: 14,
    boxSizing: "border-box",
  };

  const formSelect = {
    width: "100%",
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #d1d5db",
    background: "#fff",
    fontSize: 14,
    boxSizing: "border-box",
  };

  const modalButtons = {
    display: "flex",
    gap: 12,
    marginTop: 24,
  };

  const cancelButton = {
    background: "#f3f4f6",
    color: "#374151",
    border: "none",
    padding: "10px 16px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 500,
    fontSize: 14,
    flex: 1,
  };

  const submitButton = {
    background: "#2563eb",
    color: "#fff",
    border: "none",
    padding: "10px 16px",
    borderRadius: 8,
    cursor: "pointer",
    fontWeight: 500,
    fontSize: 14,
    flex: 1,
  };

  const handleAddAsset = async () => {
    try {
      const response = await fetch("http://localhost:8001/assets/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newAsset),
      });

      if (response.ok) {
        setShowModal(false);
        setNewAsset({
          name: "",
          type: "",
          criticality: "Medium",
          status: "Online",
          ip: "",
          owner: "",
        });
        // Refresh assets list
        fetch("http://localhost:8001/assets/", {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        })
          .then((res) => res.json())
          .then((data) => setAssets(Array.isArray(data) ? data : []));
      } else {
        const error = await response.json();
        alert(error.detail || "Failed to add asset");
      }
    } catch (err) {
      console.error("Error adding asset:", err);
      alert("Failed to add asset");
    }
  };

  return (
    <div style={page}>
      <div style={title}>Asset Management</div>
      <div style={subtitle}>
        Monitor and manage all IT assets across your healthcare infrastructure
      </div>

      {/* Top Cards */}
      <div style={cards}>
        <div style={card}>
          <div style={cardLabel}>Total Assets</div>
          <div style={cardValue}>{totalAssets}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>Online</div>
          <div style={{ ...cardValue, color: "#16a34a" }}>{onlineAssets}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>Critical Assets</div>
          <div style={{ ...cardValue, color: "#dc2626" }}>{criticalAssets}</div>
        </div>
        <div style={card}>
          <div style={cardLabel}>Compromised</div>
          <div style={{ ...cardValue, color: "#dc2626" }}>{compromisedAssets}</div>
        </div>
      </div>

      {/* Toolbar */}
      <div style={toolbar}>
        <input
          style={input}
          placeholder="Search assets by name, type, or IP..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select style={select} value={critFilter} onChange={(e) => setCritFilter(e.target.value)}>
          <option value="All">All Criticality</option>
          <option value="Critical">Critical</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
        <select style={select} value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="All">All Status</option>
          <option value="Online">Online</option>
          <option value="Secure">Secure</option>
          <option value="Compromised">Compromised</option>
          <option value="Offline">Offline</option>
        </select>
        {isAdmin && (
          <button style={buttonStyle} onClick={() => setShowModal(true)}>
            + Add Asset
          </button>
        )}
      </div>

      {/* Table */}
      <div style={tableWrap}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={th}>ASSET</th>
              <th style={th}>TYPE</th>
              <th style={th}>CRITICALITY</th>
              <th style={th}>STATUS</th>
              <th style={th}>IP ADDRESS</th>
              <th style={th}>OWNER</th>
              <th style={th}>LAST SCAN</th>
            </tr>
          </thead>
          <tbody>
            {filteredAssets.length === 0 ? (
              <tr>
                <td style={{ ...td, textAlign: "center" }} colSpan={7}>
                  No assets found
                </td>
              </tr>
            ) : (
              filteredAssets.map((a, idx) => (
                <tr key={idx}>
                  <td style={td}>{a.name || "-"}</td>
                  <td style={td}>{a.type || "-"}</td>
                  <td style={td}>{a.criticality || "-"}</td>
                  <td style={td}>{a.status || "-"}</td>
                  <td style={td}>{a.ip || "-"}</td>
                  <td style={td}>{a.owner || "-"}</td>
                  <td style={td}>-</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Add Asset Modal */}
      {showModal && (
        <div style={modalOverlay} onClick={() => setShowModal(false)}>
          <div style={modalContent} onClick={(e) => e.stopPropagation()}>
            <div style={modalTitle}>Add New Asset</div>
            
            <div style={formGroup}>
              <label style={label}>Asset Name</label>
              <input
                style={formInput}
                placeholder="Enter asset name"
                value={newAsset.name}
                onChange={(e) => setNewAsset({ ...newAsset, name: e.target.value })}
              />
            </div>

            <div style={formGroup}>
              <label style={label}>Type</label>
              <input
                style={formInput}
                placeholder="e.g., Server, Workstation, Printer"
                value={newAsset.type}
                onChange={(e) => setNewAsset({ ...newAsset, type: e.target.value })}
              />
            </div>

            <div style={formGroup}>
              <label style={label}>Criticality</label>
              <select
                style={formSelect}
                value={newAsset.criticality}
                onChange={(e) => setNewAsset({ ...newAsset, criticality: e.target.value })}
              >
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>

            <div style={formGroup}>
              <label style={label}>Status</label>
              <select
                style={formSelect}
                value={newAsset.status}
                onChange={(e) => setNewAsset({ ...newAsset, status: e.target.value })}
              >
                <option value="Online">Online</option>
                <option value="Secure">Secure</option>
                <option value="Compromised">Compromised</option>
                <option value="Offline">Offline</option>
              </select>
            </div>

            <div style={formGroup}>
              <label style={label}>IP Address</label>
              <input
                style={formInput}
                placeholder="e.g., 192.168.1.1"
                value={newAsset.ip}
                onChange={(e) => setNewAsset({ ...newAsset, ip: e.target.value })}
              />
            </div>

            <div style={formGroup}>
              <label style={label}>Owner</label>
              <input
                style={formInput}
                placeholder="Enter owner name"
                value={newAsset.owner}
                onChange={(e) => setNewAsset({ ...newAsset, owner: e.target.value })}
              />
            </div>

            <div style={modalButtons}>
              <button style={cancelButton} onClick={() => setShowModal(false)}>
                Cancel
              </button>
              <button style={submitButton} onClick={handleAddAsset}>
                Add Asset
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Assets;
